import { prisma } from '../src/client';

async function main() {
  const project = await prisma.project.upsert({
    where: { domain: 'example.com' },
    update: {},
    create: { name: 'Demo project', domain: 'example.com' },
  });

  await prisma.keyword.upsert({
    where: { projectId_term: { projectId: project.id, term: 'answer engine optimization' } },
    update: {},
    create: {
      projectId: project.id,
      term: 'answer engine optimization',
      intent: 'INFORMATIONAL',
      difficulty: 42,
      opportunity: 58,
    },
  });
}

main()
  .then(() => prisma.$disconnect())
  .catch(async (error: unknown) => {
    console.error(error);
    await prisma.$disconnect();
    process.exit(1);
  });
