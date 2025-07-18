import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import path from "path";

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [vue()],
    resolve: {
        alias: {
            "@": path.resolve(__dirname, "./src"),
        },
    },
    server: {
        host: "0.0.0.0",
        port: 5173,
        hmr: {
            port: 5173,
            // Disable HMR over network connections to avoid WebSocket issues
            // HMR will only work for localhost development
            overlay: true
        },
        watch: {
            usePolling: true, // Enable polling for Docker
            interval: 1000, // Check every second
        },
        allowedHosts: [
            "app.tdnet.xyz",
            "192.168.0.176",
            "localhost"
        ]
    },
});
