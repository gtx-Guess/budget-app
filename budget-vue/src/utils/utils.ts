import { ref } from 'vue';
import { Router } from 'vue-router';

export const message = ref<string>('');
export const showMessage = ref<boolean>(false);

/**
 * Logs message on page and re-directs if needed
 * @param text - Required, this is the text for the bubble
 * @param router - Optional, needed to re-direct. Include vue router
 * @param reRoute - Optional, needed to re-direct. Include href
 * @param duration - Optional, to set different timeout durations
 */
export const handleMessage = (text: string, router: Router | {} = {}, reRoute: string = '', duration: number = 2500): void => {
    message.value = text;
    showMessage.value = true;

    setTimeout(() => {
        showMessage.value = false;
        message.value = '';
        if (reRoute && 'push' in router) {
            router.push(reRoute);
        }
    }, duration);
};
