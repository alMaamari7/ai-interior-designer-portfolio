import {apiFetch} from "../../clients/client";
export type AuthResponse={access_token:string;user:{id:number;email:string;first_name:string;last_name:string}};
async function send(path:string,body:unknown):Promise<AuthResponse>{const r=await apiFetch(path,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});if(!r.ok){const e=await r.json();throw new Error(e.detail??"Authentication failed.")}return r.json()}
export const login=(body:unknown)=>send("/auth/login",body);export const register=(body:unknown)=>send("/auth/register",body);