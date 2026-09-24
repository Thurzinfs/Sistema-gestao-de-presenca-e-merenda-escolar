import type { User } from "../services/users";

export const USER_ROLES: { value: User['role'], label: string}[] = [
    { value: 'PENDING', label: 'Pendente'},
    { value: 'CANTEEN', label: 'Cantina'},
    { value: 'COORDINATOR', label: 'Coordenador'},
    { value: 'MONITOR', label: 'Monitor'},
    { value: 'DIRECTION', label: 'Direção'}
]
