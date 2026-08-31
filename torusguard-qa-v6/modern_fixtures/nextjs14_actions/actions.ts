"use server";

export async function deleteDocument(docId: string) {
    // Unauthenticated Next.js 14 Server Action
    await db.document.delete({ where: { id: docId } });
    return { success: true };
}
