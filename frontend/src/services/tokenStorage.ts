const ACCESS_TOKEN = 'access_token';
const REFRESH_TOKEN = 'refresh_token';

export const tokenService = {
    getAccessToken: () => localStorage.getItem(ACCESS_TOKEN),
    getRefreshToken: () => localStorage.getItem(REFRESH_TOKEN),

    saveTokens: (access: string, refresh: string) => {
        localStorage.setItem(ACCESS_TOKEN, access);
        localStorage.setItem(REFRESH_TOKEN, refresh);
    },
    clearTokens: () => {
        localStorage.removeItem(ACCESS_TOKEN);
        localStorage.removeItem(REFRESH_TOKEN);
    }
}
