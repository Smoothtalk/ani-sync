import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/transmission": { target: "http://localhost:8000", changeOrigin: false },
      "/anilist": { target: "http://localhost:8000", changeOrigin: false },
      "/sync/": {
        target: "http://localhost:8000",
        changeOrigin: false,
      },
      "/csrf/": {
        target: "http://localhost:8000",
        changeOrigin: false,
      },
      "/user/new_user": {
        target: "http://localhost:8000",
        changeOrigin: false,
      },
      "/user/login": {
        target: "http://localhost:8000",
        changeOrigin: false,
      },
      "/user/logout": {
        target: "http://localhost:8000",
        changeOrigin: false,
      },
    },
  },
});
