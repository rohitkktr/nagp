<script lang="ts">
  import { browser } from '$app/environment';

  let user = '';
  let cart: any[] = [];
  let config: { PUBLIC_CART_API: string; PUBLIC_ORDER_API: string } | null = null;

  if (browser) {
    // load config.json first
    fetch('/config.json')
      .then(res => res.json())
      .then(data => {
        config = data;
        user = localStorage.getItem('user') || '';
        fetchCart();
      })
      .catch(err => {
        console.error("Failed to load config.json:", err);
      });
  }

  async function fetchCart() {
    if (!config) return;
    try {
      const res = await fetch(`${config.PUBLIC_CART_API}/cart/${user}`);
      cart = res.ok ? await res.json() : [];
    } catch (err) {
      console.error("Failed to fetch cart:", err);
      cart = [];
    }
  }

  async function removeFromCart(index: number) {
    if (!config) return;

    // remove locally
    cart.splice(index, 1);
    cart = [...cart];

    try {
      await fetch(`${config.PUBLIC_CART_API}/cart/${user}/clear`, { method: 'DELETE' });
      for (const item of cart) {
        await fetch(`${config.PUBLIC_CART_API}/cart/${user}/add`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(item)
        });
      }
    } catch (err) {
      console.error("Failed to update cart:", err);
    }
  }

  async function placeOrder() {
    if (!config) return;

    try {
      const res = await fetch(`${config.PUBLIC_ORDER_API}/order`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: user })
      });

      const data = await res.json();
      alert(`Order ${data.status}`);
      cart = [];
    } catch (err) {
      console.error("Failed to place order:", err);
    }
  }
</script>

<h1>{user}'s Cart</h1>

{#if cart.length === 0}
  <p>Cart is empty</p>
{:else}
  {#each cart as item, i}
    <div>
      Product ID: {item.product_id} | Quantity: {item.quantity}
      <button on:click={() => removeFromCart(i)}>Remove</button>
    </div>
  {/each}

  <button on:click={placeOrder}>Place Order</button>
{/if}
