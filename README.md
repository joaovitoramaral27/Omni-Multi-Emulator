# Omni Multi-Emulator

O Omni Multi-Emulator é um projeto de multi-emulador mobile desenvolvido em Python, criado com foco em dispositivos móveis.

O projeto tem como objetivo inicialmente oferecer suporte aos consoles portáteis da Nintendo:

- Game Boy (GB)
- Game Boy Color (GBC)
- Game Boy Advance (GBA)

A arquitetura do projeto será desenvolvida pensando na expansão futura para outros sistemas, como:

- Nintendo DS
- Nintendo 3DS
- PC (para aplicações bem leves inicialmente)
- Outros consoles e plataformas no futuro

## Objetivo

O Omni Multi-Emulator busca ser um emulador modular, organizado e preparado para crescer junto com novos sistemas.

A ideia é separar a interface mobile do núcleo de emulação, permitindo que diferentes sistemas possam ser adicionados sem precisar reconstruir toda a aplicação.

## Tecnologias

O projeto será desenvolvido inicialmente utilizando:

- Python
- Kivy
- Buildozer
- Android

# Roadmap inicial

## Fase 1 • Cartucho

1. [x]Criar projeto
2. [ ]Criar App
3. [ ]Carregar ROM
4. [ ]Ler Header
5. [ ]Identificar tamanho da ROM
6. [ ]Identificar tipo de cartucho
7. [ ]Implementar MBC

## Fase 2 • Memória

8. [ ]Criar Memory Bus
9. [ ]Implementar mapa de memória
10. [ ]ROM
11. [ ]VRAM
12. [ ]WRAM
13. [ ]OAM
14. [ ]I/O
15. [ ]HRAM

## Fase 3 • CPU

16. [ ]Registradores
17. [ ]PC
18. [ ]SP
19. [ ]Flags
20. [ ]Fetch
21. [ ]Decode
22. [ ]Execute
23. [ ]Instruções 8-bit
24. [ ]Instruções 16-bit
25. [ ]Instruções CB
26. [ ]Jumps
27. [ ]Stack
28. [ ]Interrupts

## Fase 4 • PPU

29. [ ]VRAM
30. [ ]Tiles
31. [ ]Background
32. [ ]Window
33. [ ]Sprites
34. [ ]Scanlines
35. [ ]LCD

## Fase 5 • Input

36. [ ]D-Pad
37. [ ]A
38. [ ]B
39. [ ]Start
40. [ ]Select
41. [ ]L
42. [ ]R

## Fase 6 • Timers + Áudio

43. [ ]Timers
44. [ ]Áudio

## Fase 7 • Game Loop

45. [ ]Game Loop
46. [ ]Sincronização
47. [ ]Renderização
48. [ ]Input
49. [ ]Execução por frame