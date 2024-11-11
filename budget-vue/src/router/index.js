import { createRouter, createWebHistory } from "vue-router";
import HomeView from "@/views/HomeView.vue";
import ConnectToBankView from "@/views/ConnectToBank.vue";
import LoginView from "@/views/Login.vue";
import CreateUserView from "@/views/CreateUser.vue";
import axios from "axios";
const BASE_URL = import.meta.env.VITE_BACKEND_URL;
axios.defaults.withCredentials = true;

const routes = [
    {
        path: "/",
        name: "Home",
        component: HomeView,
        meta: { requiresAuth: true },
    },
    {
        path: "/connect",
        name: "Bank Connection Page",
        component: ConnectToBankView,
        meta: { requiresAuth: true },
    },
    {
        path: "/login",
        name: "Login Page",
        component: LoginView,
        meta: { hideNavbar: true },
    },
    {
        path: "/create",
        name: "Create User Page",
        component: CreateUserView,
        meta: { hideNavbar: true },
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

router.beforeEach(async (to, from, next) => {
    if (to.meta.requiresAuth) {
        const resp = await axios.post(`${BASE_URL}/authenticated`);
        const authApiResponse = resp.data;
        if (authApiResponse.status === 200) {
            next();
        } else {
            try {
                const refreshApiResp = await axios.post(`${BASE_URL}/refresh_token`);
                if(refreshApiResp.status === 200){
                    next();
                }else{
                    next("/login");
                };
            } catch (refreshError) {
                next("/login");
            };
        };
    } else {
        next();
    };
});

export default router;
