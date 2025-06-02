import { createRouter, createWebHistory } from "vue-router";
import HomeView from "@/views/HomeView.vue";
import ConnectToBankView from "@/views/ConnectToBank.vue";
import LoginView from "@/views/Login.vue";
import CreateUserView from "@/views/CreateUser.vue";
import ProfileView from "@/views/Profile.vue";
import TransactionsView from "@/views/Transactions.vue";
import axios from "axios";

const routes = [
    {
        path: "/",
        name: "Home",
        component: HomeView,
        meta: { requiresAuth: true, showNavbar: true },
    },
    {
        path: "/profile",
        name: "Profile",
        component: ProfileView,
        meta: { requiresAuth: true, showNavbar: true},
    },
    {
        path: "/transactions",
        name: "Transactions",
        component: TransactionsView,
        meta: { requiresAuth: true, showNavbar: true},
    },
    {
        path: "/connect",
        name: "Bank Connection Page",
        component: ConnectToBankView,
        meta: { requiresAuth: true, showNavbar: true },
    },
    {
        path: "/login",
        name: "Login Page",
        component: LoginView,
        meta: { requiresAuth: false, showNavbar: false },
    },
    {
        path: "/create",
        name: "Create User Page",
        component: CreateUserView,
        meta: { requiresAuth: false, showNavbar: false },
    },
    { path: '/:catchAll(.*)', redirect: '/' }
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

router.beforeEach(async (to, from, next) => {
    if (to.meta.requiresAuth) {
        try {
            const resp = await axios.post('/api/authenticated');
            if (resp.data.status === 200) {
                next();
            } else {
                next("/login");
            }
        } catch (error) {
            next("/login");
        }
    } else {
        next();
    }
});

export default router;
