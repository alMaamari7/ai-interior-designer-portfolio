const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";
export async function apiFetch(endpoint:string, options:RequestInit={}){
 const token=localStorage.getItem("token"); const headers=new Headers(options.headers);
 if(token) headers.set("Authorization",`Bearer ${token}`);
 const response=await fetch(`${API_BASE_URL}${endpoint}`,{...options,headers});
 if(response.status===401){localStorage.removeItem("token");localStorage.removeItem("user");window.location.href="/login";}
 return response;
}
export function buildImageUrl(path:string){return `${API_BASE_URL}/uploads/${path}`;}