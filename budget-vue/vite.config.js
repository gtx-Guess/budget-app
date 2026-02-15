import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import path from "path";

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
            protocol: 'wss',
            host: 'app.tdnet.xyz',
            clientPort: 443,
            port: 5173
        },
        watch: {
            usePolling: true,
            interval: 1000,
        },
        allowedHosts: [
            "app.tdnet.xyz",
            "192.168.0.176",
            "localhost"
        ]
    },
});