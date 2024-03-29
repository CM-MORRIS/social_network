import axios from 'axios'

const baseURL = 'http://127.0.0.1:8000/api-auth/'

const axiosInstance = axios.create({
    baseURL: baseURL,
    timeout: 5000,
    headers: {
        'Authorization': localStorage.getItem('access_token') ? "JWT " + localStorage.getItem('access_token') : null,
        'Content-Type': 'application/json',
        'accept': 'application/json'
    }
});

axiosInstance.interceptors.response.use(
    response => response,
    async error => {

        const originalRequest = error.config;
        console.log("3");

        // Prevent infinite loops
        const tokenRefreshUrl = "/token/refresh/"

        console.log("originalRequest.url: " + originalRequest.url)
        console.log("tokenRefreshUrl: " + tokenRefreshUrl)

        if (error.response.status == "401" && originalRequest.url == tokenRefreshUrl) {

            window.location.href = '/login/';
            console.log("2");

            return Promise.reject(error);
        }

        if (error.response.data.code == "token_not_valid" &&
            error.response.status == "401" && 
            error.response.statusText == "Unauthorized") 
            {
                console.log("4");

                const refreshToken = localStorage.getItem('refresh_token');

                if (refreshToken) {
                    const tokenParts = JSON.parse(atob(refreshToken.split('.')[1]));

                    // exp date in token is expressed in seconds, while now() returns milliseconds:
                    const now = Math.ceil(Date.now() / 1000);
                    console.log("1");
                    console.log(tokenParts.exp);

                    if (tokenParts.exp > now) {
                        console.log("5");

                        try {
                            const response = await axiosInstance.post('/token/refresh/', { 
                                refresh: refreshToken 
                            });

                            localStorage.setItem('access_token', response.data.access);
                            localStorage.setItem('refresh_token', response.data.refresh);

                            axiosInstance.defaults.headers['Authorization'] = "JWT " + response.data.access;
                            originalRequest.headers['Authorization'] = "JWT " + response.data.access;

                            return await axiosInstance(originalRequest);

                        } catch (err) {

                            console.log("6");
                            console.log(err);
                        }
                    }
                    else {
                        console.log("Refresh token is expired", tokenParts.exp, now);
                        window.location.href = '/login/';
                        console.log("7");

                    }
                }
                else {
                    console.log("Refresh token not available.")
                    window.location.href = '/login/';
                    console.log("8");

                }
        }
      
      // specific error handling done elsewhere
      return Promise.reject(error);
  }
);

export default axiosInstance