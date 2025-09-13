import adapter from '@sveltejs/adapter-static';
import preprocess from 'svelte-preprocess';

const config = {
  preprocess: preprocess(),
  kit: {
    adapter: adapter({
      // fallback for SPA routing
      fallback: 'index.html'
    }),
    paths: {
      base: ''
    }
  }
};

export default config;