import { useLocalStore } from '@/stores/localStorage'

/**
 * This is used to load data that should be ready on app init.
 * Should be ran before the app mounts but after all required resources are ready
 */
export const initializeApp = async () => {
    const store = useLocalStore();
    await store.getCategories();
};