import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/transmission": { target: "http://localhost:8000", changeOrigin: false },
      "/anilist": { target: "http://localhost:8000", changeOrigin: false },
    },
  },
});
