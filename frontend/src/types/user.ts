export interface User {
    id: number;
    name: string;
    email: string;
    password: string;
    number: string;
    role: 'admin' | 'user' | 'canteen' | 'teacher' | 'manager';
}
