/*
  Warnings:

  - Added the required column `className` to the `Note` table without a default value. This is not possible if the table is not empty.

*/
-- DropForeignKey
ALTER TABLE "Note" DROP CONSTRAINT "Note_uploaded_by_fkey";

-- AlterTable
ALTER TABLE "Note" ADD COLUMN     "className" TEXT NOT NULL,
ALTER COLUMN "uploaded_by" SET DATA TYPE TEXT;
