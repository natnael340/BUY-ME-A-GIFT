import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api",
});
const _api = axios.create({
  baseURL: "http://127.0.0.1:8000/api",
});
api.interceptors.request.use(
  async (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers["Authorization"] = `Bearer ${token}`;
      try {
        await api.post("/token/verify", {
          token,
        });
        return config;
      } catch (error: any) {
        if (error.response.status === 401) {
          console.log("Token expired, refreshing...");
          const refreshToken = localStorage.getItem("refreshToken");
          if (refreshToken) {
            try {
              const response = await api.post("/refresh", {
                refresh: refreshToken,
              });
              const newToken = response.data.access;
              localStorage.setItem("token", newToken);
              config.headers["Authorization"] = `Bearer ${newToken}`;
              return config;
            } catch (error) {
              console.log("Refresh failed, redirecting to login...");
              window.location.href = "/login";
            }
          } else {
            console.log("Refresh token not found, redirecting to login...");
            window.location.href = "/login";
          }
        } else {
          console.log("Error:", error.message);
        }
      }
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export const getProducts = async () => {
  try {
    const { data } = await _api.get("/products");
    return data;
  } catch (error) {
    return [];
  }
};
export const addProduct = (data: any) => {
  return api.post("/products/add", data);
};
export const login = (data: { email: string; password: string }) => {
  return api.post("/user/login", data);
};
export const signup = (data: { email: string; password: string }) => {
  return api.post("/user/signup", data);
};
export const wishlist = () => {
  return api.get("/user/wishlist");
};
export const addToWishlist = (product: any) => {
  return api.post("/user/wishlist/add", product);
};
