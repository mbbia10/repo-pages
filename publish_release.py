import sys
import os
from datetime import datetime
from github import Github # Importando a biblioteca PyGithub

def publicar_no_pages(mensagem_release):
    # 1. Configurações e Segredos
    token = os.getenv("GITHUB_TOKEN")
    repo_name = "mbbia10/repo-pages" # <--- TROQUE PELO SEU REPOSITÓRIO
    file_path = "changelog.md" # O arquivo que o GitHub Pages vai ler

    if not token:
        print("❌ Erro: Variável GITHUB_TOKEN não encontrada.")
        return

    try:
        print("🔄 Conectando à API do GitHub...")
        # Autenticação
        g = Github(token)
        repo = g.get_repo(repo_name)

        # 2. Tenta buscar o arquivo existente
        # Precisamos do 'sha' (hash) do arquivo para ter permissão de editá-lo
        try:
            contents = repo.get_contents(file_path)
            conteudo_atual = contents.decoded_content.decode("utf-8")
            sha_arquivo = contents.sha
            print(f"📂 Arquivo {file_path} encontrado. Atualizando...")
        except:
            # Se o arquivo não existir, cria um novo
            conteudo_atual = "# Histórico de Versões\n\n"
            sha_arquivo = None # Sem SHA pois é criação
            print(f"⚠️ Arquivo {file_path} não encontrado. Criando novo...")

        # 3. Formata o novo conteúdo (Markdown)
        # Adiciona a data e a mensagem no TOPO do conteúdo existente
        data_hoje = datetime.now().strftime("%d/%m/%Y %H:%M")
        nova_entrada = f"## 🚀 Release - {data_hoje}\n{mensagem_release}\n\n---\n\n"
        
        novo_conteudo_completo = nova_entrada + conteudo_atual

        # 4. Realiza o Commit via API
        commit_msg = f"docs: atualiza release notes via script - {data_hoje}"

        if sha_arquivo:
            # Update (requer o SHA do arquivo original)
            repo.update_file(file_path, commit_msg, novo_conteudo_completo, sha_arquivo)
        else:
            # Create
            repo.create_file(file_path, commit_msg, novo_conteudo_completo)

        print("✅ Sucesso! O GitHub Pages deve atualizar em instantes.")

    except Exception as e:
        print(f"❌ Falha ao publicar no GitHub: {e}")

if __name__ == "__main__":
    # Validação de argumentos
    if len(sys.argv) < 2:
        print("Uso incorreto. Execute: python publish_release.py 'Texto da Release'")
    else:
        msg = sys.argv[1]
        publicar_no_pages(msg)