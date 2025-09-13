<script lang="ts">
  import { goto } from '$app/navigation';
  import { browser } from '$app/environment';

  let username = '';
  let password = '';
  let error = '';
  let config: { PUBLIC_AUTH_API: string } | null = null;

  if (browser) {
    // load config.json
    fetch('/config.json')
      .then(res => res.json())
      .then(data => {
        config = data;
      })
      .catch(err => {
        console.error("Failed to load config.json:", err);
        error = "Configuration error. Please try again later.";
      });
  }

  async function login() {
    if (!config) {
      error = "API not configured";
      return;
    }

    try {
      const res = await fetch(`${config.PUBLIC_AUTH_API}/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      });

      if (res.ok) {
        localStorage.setItem('user', username);
        goto('/products');
      } else {
        const err = await res.json();
        error = err.detail || 'Login failed';
      }
    } catch (err) {
      console.error("Login request failed:", err);
      error = "Network error. Please try again.";
    }
  }
</script>

<h1>Login</h1>
<div>
  <input placeholder="Username" bind:value={username} />
</div>
<div>
  <input type="password" placeholder="Password" bind:value={password} />
</div>
<div>
  <button on:click={login}>Login</button>
</div>
<p style="color:red">{error}</p>
