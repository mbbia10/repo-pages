import sys
import os
from datetime import datetime
from github import Github
from github import Auth


def publicar_no_pages(mensagem_release: str):
    # 1️⃣ Segurança: Token via variável de ambiente
    token = os.getenv("GITHUB_TOKEN")
    repo_name = "mbbia10/repo-pages"  # ✅ Seu repositório
    file_path = "changelog.md"

    if not token:
        print("❌ Erro: Variável de ambiente GITHUB_TOKEN não encontrada.")
        sys.exit(1)

    try:
        print("🔄 Conectando à API do GitHub...")

        # 🔐 Nova forma correta (sem warning de deprecated)
        auth = Auth.Token(token)
        g = Github(auth=auth)

        repo = g.get_repo(repo_name)

        # 2️⃣ Buscar arquivo existente
        try:
            contents = repo.get_contents(file_path)
            conteudo_atual = contents.decoded_content.decode("utf-8")
            sha_arquivo = contents.sha
            print(f"📂 Arquivo {file_path} encontrado. Atualizando...")
        except Exception:
            print(f"⚠️ Arquivo {file_path} não encontrado. Criando novo...")
            conteudo_atual = "# 📜 Histórico de Versões\n\n"
            sha_arquivo = None

        # 3️⃣ Criar nova entrada
        data_hoje = datetime.now().strftime("%d/%m/%Y %H:%M")

        nova_entrada = (
            f"## 🚀 Release - {data_hoje}\n\n"
            f"{mensagem_release}\n\n"
            f"---\n\n"
        )

        novo_conteudo = nova_entrada + conteudo_atual

        commit_msg = f"docs: atualiza release notes via script - {data_hoje}"

        # 4️⃣ Commit via API
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
    if len(sys.argv) < 2:
        print("Uso: python publish_release.py \"Texto da Release\"")
        sys.exit(1)

    mensagem = sys.argv[1]
    publicar_no_pages(mensagem)