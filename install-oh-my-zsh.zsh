#!/data/data/com.termux/files/usr/bin/zsh

export ZSH="/data/community/.oh-my-zsh"
export ZSH_CUSTOM="/data/community/.oh-my-zsh/custom"
if [ ! -f /data/community/.p10k.zsh ]; then
    cp /data/community/.oh-my-comma/default-bashrcs/.p10k.zsh /data/community/.p10k.zsh
    if [ -f ~/.p10k.zsh ]; then
        rm ~/.p10k.zsh
    fi
    ln -s /data/community/.p10k.zsh ~/.p10k.zsh
fi
curl https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh --output /data/community/install-ohmyzsh.sh
chmod +x /data/community/install-ohmyzsh.sh
ZSH="/data/community/.oh-my-zsh" sh /data/community/install-ohmyzsh.sh --unattended
rm /data/community/install-ohmyzsh.sh
mv ~/.zshrc /data/community/.zshrc
ln -s /data/community/.zshrc ~/.zshrc
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM}/themes/powerlevel10k
sed -i '/^# Path to your oh-my-zsh installation./d' ~/.zshrc
sed -i '/^export ZSH=/d' ~/.zshrc
sed -i '1iexport ZSH="/data/community/.oh-my-zsh"\nexport ZSH_CUSTOM="/data/community/.oh-my-zsh/custom"\nexport HISTFILE=/data/community/.zsh_history\nZDOTDIR=/data/community\n' ~/.zshrc
rm -rf /home/.oh-my-zsh
ln -s /data/community/.oh-my-zsh /home/.oh-my-zsh
ln -s /data/community/.zsh_history ~/.zsh_history
echo 'POWERLEVEL9K_DISABLE_CONFIGURATION_WIZARD=true' >>! ~/.zshrc
sed -i 's/^ZSH_THEME=".\+"$/ZSH_THEME=\"powerlevel10k\/powerlevel10k\"/g' ~/.zshrc
mv ~/.zshrc /data/community/.zshrc
ln -s /data/community/.zshrc ~/.zshrc
echo "Do you want to make zsh default in terminal sessions by starting zsh from your .bashrc?"
read -p "[Y/n] > " choices
case ${choices} in
y|Y ) sed -i '/^zsh/d' /data/community/.bashrc && echo '/data/data/com.termux/files/usr/bin/zsh' >> /data/community/.bashrc;;
* ) echo "Skipping...";;
esac
