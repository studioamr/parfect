-- PARFECT · tabla de waitlist
-- Pega TODO esto en Supabase → SQL Editor → Run (1 vez)
create table if not exists public.waitlist (
  id uuid primary key default gen_random_uuid(),
  nombre text,
  correo text unique not null,
  fuente text,
  created_at timestamptz default now()
);
alter table public.waitlist enable row level security;
-- cualquiera puede APUNTARSE, nadie puede LEER la lista (solo tú desde el panel)
create policy "waitlist_insert_anon" on public.waitlist
  for insert to anon with check (true);
