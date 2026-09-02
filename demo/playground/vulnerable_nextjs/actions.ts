/**
 * TorusGuard Playground: Vulnerable Next.js Server Action Fixture
 * Contains 2 intentional security findings for demonstration purposes:
 *   - TG-CLIENT-001 (Leaked Service Role Key)
 *   - TG-AUTH-003 (Unauthenticated Server Action Mutation)
 */

// Finding 1: TG-CLIENT-001 - Backend admin key exposed in client-accessible code
export const SUPABASE_SERVICE_ROLE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.demo_secret_token_1234567890";

interface UserRecord {
  id: string;
  role: string;
}

// Finding 2: TG-AUTH-003 - Server Action performing state change without session check
export async function updateUserRole(userId: string, newRole: string): Promise<{ success: boolean }> {
  "use server";

  // VULNERABLE: Lacks auth session check e.g. const session = await auth(); if (!session?.user?.isAdmin) throw ...
  console.log(`[VULNERABLE] Updating user ${userId} to role ${newRole} without authentication check`);
  
  return { success: true };
}
