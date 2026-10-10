let refreshToken = null

const tokenManager = {
    getAccessToken() {
        return sessionStorage.getItem("access_token")
    },

    setAccessToken(token) {
        sessionStorage.setItem("access_token", token)
    },

    getRefreshToken() {
        return refreshToken
    },

    setRefreshToken(token) {
        refreshToken = token
    },

    clearTokens() {
        sessionStorage.removeItem("access_token")
        refreshToken = null
    },
}

export default tokenManager