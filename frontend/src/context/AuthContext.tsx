import {createContext,useState,type ReactNode} from "react";
type User={id:number;email:string;first_name:string;last_name:string};
type AuthResponse={access_token:string;user:User};
type Ctx={user:User|null;token:string|null;isAuthenticated:boolean;login:(r:AuthResponse)=>void;logout:()=>void};
export const AuthContext=createContext<Ctx|undefined>(undefined);
export function AuthProvider({children}:{children:ReactNode}){
 const [user,setUser]=useState<User|null>(()=>{const v=localStorage.getItem("user");return v?JSON.parse(v):null});
 const [token,setToken]=useState<string|null>(()=>localStorage.getItem("token"));
 function login(r:AuthResponse){setUser(r.user);setToken(r.access_token);localStorage.setItem("user",JSON.stringify(r.user));localStorage.setItem("token",r.access_token)}
 function logout(){setUser(null);setToken(null);localStorage.removeItem("user");localStorage.removeItem("token")}
 return <AuthContext.Provider value={{user,token,isAuthenticated:token!==null,login,logout}}>{children}</AuthContext.Provider>
}