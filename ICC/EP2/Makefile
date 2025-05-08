# PROGRAMA
PROG = resolveEDO
OBJS = resolveEDO.o edo.o utils.o lu.o

# Compilador
CC = gcc

# Diretórios do LIKWID (assume que estão definidos no ambiente)
# Exemplo:
# export LIKWID_INCLUDE=/usr/local/include
# export LIKWID_LIB=/usr/local/lib

# Flags de compilação: inclui suporte a LIKWID Marker API
CFLAGS = -O0 -DLIKWID_PERFMON -I${LIKWID_INCLUDE}

# Flags de linkagem: inclui matemática e biblioteca LIKWID
LFLAGS = -lm -L${LIKWID_LIB} -llikwid

# Arquivos para distribuição
DISTFILES = *.c *.h LEIAME* Makefile edos.dat
DISTDIR = ${EP2}	

.PHONY: clean purge dist all

# Compilação de cada .o
%.o: %.c %.h utils
	$(CC) -c $(CFLAGS) -o $@ $<

# Compilação final do executável
all: $(PROG)

$(PROG): $(OBJS)
	$(CC) $(CFLAGS) -o $@ $^ $(LFLAGS)

# Limpeza básica
clean:
	@echo "Limpando sujeira ..."
	@rm -f *~ *.bak

# Limpeza total
purge: clean
	@echo "Limpando tudo ..."
	@rm -f $(PROG) $(OBJS) core a.out $(DISTDIR) $(DISTDIR).tgz

# Geração de pacote para submissão
dist: purge
	@echo "Gerando arquivo de distribuição ($(DISTDIR).tgz) ..."
	@ln -s . $(DISTDIR)
	@tar -chvzf $(DISTDIR).tgz $(addprefix ./$(DISTDIR)/, $(DISTFILES))
	@rm -f $(DISTDIR)
