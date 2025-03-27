import path from "path"
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from 'tailwindcss'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react()
  ],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    proxy: {
      "/solr": {
        target: "http://localhost:8983", // Solr server
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/solr/, ""), // Rewrite the URL
      },
    },
  },
  css: {
    postcss: {
      plugins: [tailwindcss()],
    },
  }
})
