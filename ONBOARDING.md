### 1

Primeiramente, é preciso ter o git e o uv instalado na máquina. Após isso, é necessário abrir o powershell em uma pasta onde se deseja colocar o projeto e realizar os comandos abaixo:

git clone https://github.com/petrosbarreto/sistema-biblioteca-qa.git
cd sistema-biblioteca-qa
uv venv --python 3.13
uv pip install -r requirements.txt
uv run pytest -q

### 2

R1 | O exemplar só pode estar emprestado a um leitor por vez | O que acontece se uma pessoa tentar emprestar um exemplar que já está emprestado para outro leitor?

R2 | O prazo depende da categoria do leitor e do tipo de título | O sistema calcula corretamente o prazo de devolução para cada combinação de categoria de leitor e tipo de título?

R3 | Leitor com multa acima do limite não retira novo exemplar | O que acontece se um leitor com multa acima do limite tentar realizar um novo empréstimo?

R4 | Reserva vira empréstimo quando o exemplar é devolvido | Quando um exemplar reservado é devolvido, a reserva é realmente convertida em empréstimo para o leitor correto?

R5 | Periódico não tem ISBN; livro tem, e é único | O sistema impede um periódico de ter ISBN e impede que dois livros diferentes tenham o mesmo ISBN?

R6 | Histórico de empréstimo nunca é apagado | Depois que um empréstimo é encerrado ou um exemplar sofre alguma alteração, o empréstimo antigo continua aparecendo no histórico?

R7 | Exemplar danificado sai de circulação sem sair do acervo | Quando um exemplar é marcado como danificado, ele continua registrado no acervo, mas deixa de poder ser emprestado?

R8 | O mesmo título pode ter exemplares em unidades diferentes | O sistema permite que exemplares do mesmo título pertençam a unidades diferentes e mostra corretamente em qual unidade cada exemplar está?

### 3

Caracteristica | Tipo de defeito capturado

Adequação funcional | Captura defeitos em que o sistema não faz o que deveria fazer, faz de forma incorreta ou deixa de atender alguma necessidade do usuário.

Eficiência de desempenho | Captura defeitos relacionados a lentidão, uso excessivo de recursos ou incapacidade de suportar a carga esperada.

Compatibilidade | Captura defeitos em que o sistema não consegue coexistir ou trocar informações corretamente com outros sistemas.

Usabilidade | Captura defeitos que tornam o sistema difícil de entender, aprender ou utilizar, aumentando a chance de erros do usuário.

Confiabilidade | Captura defeitos que fazem o sistema falhar, ficar indisponível ou não se recuperar adequadamente de problemas.

Segurança | Captura defeitos que permitem acesso, alteração ou exposição indevida de dados e funcionalidades.

Manutenibilidade | Captura defeitos que tornam o software difícil de analisar, modificar, testar ou corrigir sem causar novos problemas.

Portabilidade | Captura defeitos que dificultam instalar, adaptar ou executar o sistema em ambientes diferentes.