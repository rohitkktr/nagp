<script lang="ts">
  import { browser } from '$app/environment';

  let user = '';
  let orders: any[] = [];
  let config: { PUBLIC_ORDER_API: string } | null = null;

  if (browser) {
    // load config.json first
    fetch('/config.json')
      .then(res => res.json())
      .then(data => {
        config = data;
        user = localStorage.getItem('user') || '';
        fetchOrders();
      })
      .catch(err => {
        console.error("Failed to load config.json:", err);
      });
  }

  async function fetchOrders() {
    if (!config) return;
    try {
      const res = await fetch(`${config.PUBLIC_ORDER_API}/order/${user}`);
      if (res.ok) {
        const data = await res.json();
        orders = data.orders || [];
      } else {
        orders = [];
      }
    } catch (err) {
      console.error("Failed to fetch orders:", err);
      orders = [];
    }
  }
</script>

<h1>{user}'s Orders</h1>

{#if orders.length === 0}
  <p>No orders yet.</p>
{:else}
  {#each orders as order}
    <div>
      Status: {order.status}
      {#if order.reason}
        | Reason: {order.reason}
      {/if}
    </div>
  {/each}
{/if}
