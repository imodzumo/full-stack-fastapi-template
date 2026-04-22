import type { UserPublic } from "@/client"

type Role = UserPublic["role"]

export const USER_ROLES = ["admin", "manager", "member"] as const satisfies Role[]

export const canListUsers = (user?: UserPublic | null) =>
  user?.role === "admin" || user?.role === "manager"

export const canCreateUsers = (user?: UserPublic | null) =>
  user?.role === "admin"

export const canManageUsers = canCreateUsers

export const canViewMetrics = canListUsers
