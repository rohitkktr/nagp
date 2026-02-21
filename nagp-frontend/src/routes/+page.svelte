<script lang="ts">
  import { goto } from '$app/navigation';
  import { browser } from '$app/environment';

  let username = '';
  let password = '';
  let error = '';
  let isLoading = false;
  let config: { PUBLIC_AUTH_API: string } | null = null;
  let configLoaded = false;

  if (browser) {
    // load config.json with retry logic
    async function loadConfig() {
      let retries = 3;
      while (retries > 0) {
        try {
          const res = await fetch('/config.json');
          if (!res.ok) throw new Error(`HTTP ${res.status}`);
          config = await res.json();
          configLoaded = true;
          console.log("Config loaded:", config);
          return;
        } catch (err) {
          console.error(`Failed to load config.json (${4 - retries}):`, err);
          retries--;
          if (retries > 0) {
            await new Promise(resolve => setTimeout(resolve, 1000)); // wait 1s before retry
          }
        }
      }
      error = "Failed to load configuration. Please refresh the page.";
      configLoaded = true;
    }
    loadConfig();
  }

  async function login() {
    if (!configLoaded) {
      error = "Configuration is loading... Please wait.";
      return;
    }

    if (!config) {
      error = "API not configured";
      return;
    }

    if (!username || !password) {
      error = "Please enter username and password";
      return;
    }

    isLoading = true;
    error = '';

    try {
      console.log("Attempting login to:", `${config.PUBLIC_AUTH_API}/login`);
      const res = await fetch(`${config.PUBLIC_AUTH_API}/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
        mode: 'cors'
      });

      if (res.ok) {
        const data = await res.json();
        localStorage.setItem('user', username);
        goto('/products');
      } else {
        const err = await res.json();
        error = err.detail || `Login failed (${res.status})`;
      }
    } catch (err) {
      console.error("Login request failed:", err);
      error = `Network error. Please check if the auth service is running. ${err instanceof Error ? err.message : ''}`;
    } finally {
      isLoading = false;
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
