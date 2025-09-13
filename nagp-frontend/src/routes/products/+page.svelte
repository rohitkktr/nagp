<script lang="ts">
  import { browser } from '$app/environment';

  let user = '';
  let products: any[] = [];
  let config: { PUBLIC_PRODUCT_API: string; PUBLIC_CART_API: string } | null = null;
  let loading = true;

  if (browser) {
    init();
  }

  async function init() {
    try {
      // load config.json
      const res = await fetch('/config.json');
      config = await res.json();

      // load user
      user = localStorage.getItem('user') || '';

      // fetch products
      await fetchProducts();
    } catch (err) {
      console.error("❌ Failed to initialize:", err);
    } finally {
      loading = false;
    }
  }

  async function fetchProducts() {
    if (!config) return;
    try {
      const res = await fetch(`${config.PUBLIC_PRODUCT_API}/products`);
      products = res.ok ? await res.json() : [];
    } catch (err) {
      console.error("❌ Failed to fetch products:", err);
      products = [];
    }
  }

  async function addToCart(product: any) {
    if (!user) return alert('⚠️ Please login first');
    if (!config) return;

    try {
      const res = await fetch(`${config.PUBLIC_CART_API}/cart/${user}/add`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ product_id: product.id, quantity: 1 })
      });

      if (res.ok) {
        alert(`✅ Added to cart: ${product.name}`);
      } else {
        alert('❌ Failed to add to cart');
      }
    } catch (err) {
      console.error("❌ Failed to add to cart:", err);
    }
  }
</script>

<h1>Welcome to Products Page</h1>
<p>Logged in as: {user}</p>

{#if loading}
  <p>Loading products...</p>
{:else if products.length === 0}
  <p>No products available</p>
{:else}
  {#each products as product}
    <div>
      {product.name} - ${product.price}
      <button disabled={!product.in_stock} on:click={() => addToCart(product)}>
        {product.in_stock ? 'Add to Cart' : 'Out of stock'}
      </button>
    </div>
  {/each}
{/if}
