<script lang="ts">
  import { goto } from '$app/navigation';
  import { onMount } from 'svelte';
  import { writable } from 'svelte/store';

  // Store for user (so it's reactive across pages)
  export const userStore = writable<string | null>(null);

  onMount(() => {
    const u = localStorage.getItem('user');
    userStore.set(u);
  });

  function logout() {
    localStorage.removeItem('user');
    userStore.set(null);
    goto('/'); // redirect to login page
  }
</script>

<header>
  <nav>
    <a href="/products">Products</a>
    <a href="/cart">Cart</a>
    <a href="/orders">Orders</a>
    {#if $userStore}
      <button on:click={logout}>Logout</button>
    {/if}
  </nav>

  <h1>NAGP Assignment</h1>
</header>

<hr />

<slot />
