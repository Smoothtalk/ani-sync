import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/transmission": "http://localhost:8000",
      "/anilist": "http://localhost:8000",
    },
  },
});
