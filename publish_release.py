import sys
import os
from datetime import datetime
from github import Github
from github import Auth


def publicar_no_pages(mensagem_release: str):

    # 🔐 Token via variável de ambiente
    token = os.getenv("GITHUB_TOKEN")
    repo_name = "mbbia10/repo-pages"
    file_path = "changelog.md"

    HEADER = "# 📜 Histórico de Versões\n\n------------------------------------\n\n"

    if not token:
        print("❌ Erro: Variável de ambiente GITHUB_TOKEN não encontrada.")
        sys.exit(1)

    try:
        print("🔄 Conectando à API do GitHub...")

        auth = Auth.Token(token)
        g = Github(auth=auth)

        repo = g.get_repo(repo_name)

        # 📂 Buscar arquivo existente
        try:
            contents = repo.get_contents(file_path)
            conteudo_atual = contents.decoded_content.decode("utf-8")
            sha_arquivo = contents.sha
            print(f"📂 Arquivo {file_path} encontrado. Atualizando...")
        except Exception:
            print(f"⚠️ Arquivo {file_path} não encontrado. Criando novo...")
            conteudo_atual = HEADER
            sha_arquivo = None

        # Garantir header correto
        if not conteudo_atual.startswith(HEADER):
            conteudo_atual = HEADER + conteudo_atual

        # 📅 Data da release
        data_hoje = datetime.now().strftime("%d/%m/%Y %H:%M")

        nova_entrada = (
            f"## 🚀 Release - {data_hoje}\n\n"
            f"{mensagem_release}\n\n"
            f"---\n\n"
        )

        # 🚫 Evitar duplicação
        if nova_entrada in conteudo_atual:
            print("⚠️ Essa release já existe no changelog.")
            return

        # 📌 Adicionar no topo mantendo header
        conteudo_sem_header = conteudo_atual.replace(HEADER, "")
        novo_conteudo = HEADER + nova_entrada + conteudo_sem_header

        commit_msg = f"docs: atualiza release notes via script - {data_hoje}"

        # 📤 Commit via API
        if sha_arquivo:
            repo.update_file(
                path=file_path,
                message=commit_msg,
                content=novo_conteudo,
                sha=sha_arquivo,
            )
        else:
            repo.create_file(
                path=file_path,
                message=commit_msg,
                content=novo_conteudo,
            )

        print("✅ Release publicada com sucesso!")
        print(f"🔗 https://github.com/{repo_name}/blob/main/{file_path}")

    except Exception as e:
        print(f"❌ Falha ao publicar no GitHub: {e}")
        sys.exit(1)


if __name__ == "__main__":

    # 🧪 Validação do argumento obrigatório
    if len(sys.argv) < 2:
        print("Uso: python publish_release.py \"Texto da Release\"")
        sys.exit(1)

    mensagem = sys.argv[1]
    publicar_no_pages(mensagem)