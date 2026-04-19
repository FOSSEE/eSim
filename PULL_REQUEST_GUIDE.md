# Pull Request Guide – eSim RAGbot Enhancements

## 1. Git Configuration (Done ✓)

- **Email:** `harvi.bhavinpatel2024@vitstudent.ac.in`
- **Name:** `Harvi-2215`

## 2. Create Your Fork on GitHub

If you don't have a fork yet:

1. Go to **[https://github.com/FOSSEE/eSim](https://github.com/FOSSEE/eSim)**
2. Click **Fork** (top right)
3. Choose your account (ensure you're logged in as the account for `harvi.bhavinpatel2024@vitstudent.ac.in`)
4. The fork will be created at `https://github.com/YOUR_USERNAME/eSim`

**Note:** Your GitHub username may be `Harvi-2215` or `HraviPatel` – use whichever matches your account.

## 3. Add Your Fork as Remote (if needed)

```powershell
cd C:\Users\91900\Downloads\eSIM-Software-AIChatBot\repos\eSim

# If using Harvi-2215:
git remote add harvi-fork https://github.com/Harvi-2215/eSim.git

# OR if using HraviPatel (already exists as hravipatel):
# git remote add hravipatel https://github.com/HraviPatel/eSim.git
```

## 4. Push Your Branch to the Fork

```powershell
cd C:\Users\91900\Downloads\eSIM-Software-AIChatBot\repos\eSim

# Push to Harvi-2215 fork:
git push harvi-fork esim-RAGbot-enhacements:esim-RAGbot-Enhacements-Harvi

# OR push to HraviPatel fork:
git push hravipatel esim-RAGbot-enhacements:esim-RAGbot-Enhacements-Harvi
```

When prompted, sign in with `harvi.bhavinpatel2024@vitstudent.ac.in` (or your GitHub credentials).

## 5. Create the Pull Request

1. Open your fork: `https://github.com/YOUR_USERNAME/eSim`
2. You should see a banner: **"esim-RAGbot-Enhacements-Harvi had recent pushes"** with a **Compare & pull request** button
3. Click **Compare & pull request**
4. Set:
   - **Base repository:** `FOSSEE/eSim`
   - **Base branch:** `master` (or `main` if that's the default)
   - **Head repository:** `YOUR_USERNAME/eSim`
   - **Compare branch:** `esim-RAGbot-Enhacements-Harvi`
5. Add a title, e.g. **"Copilot enhancements: RAG threshold, netlist contract, PaddleOCR, copy button"**
6. Add a description of the changes
7. Click **Create pull request**

## 6. Changes Included in This Branch

| File | Change |
|------|--------|
| `.gitignore` | Added `scripts/deploy_to_vm.ps1` |
| `scripts/launch_esim.sh` | Vosk model path auto-detection |
| `src/chatbot/image_handler.py` | PaddleOCR error message |
| `src/chatbot/knowledge_base.py` | RAG relevance threshold |
| `src/frontEnd/Chatbot.py` | Netlist contract bundling, copy-to-clipboard |
| `scripts/README_TESTS.md` | Test instructions and deploy steps |
| `scripts/deploy_to_vm.ps1.example` | Deploy script template |
| `scripts/test_copilot_enhancements.py` | Enhancement tests |
| `scripts/test_copilot_enhancements.sh` | Shell wrapper for tests |

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Push asks for credentials | Use GitHub CLI (`gh auth login`) or Git Credential Manager |
| "Repository not found" | Create the fork on GitHub first (Step 2) |
| Wrong GitHub account | Check `git config user.email` and ensure it matches your GitHub email |
