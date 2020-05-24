# color_transfer

Color Transfer Between images[^1]の実装をしました．
入力画像の色味を参照画像の色味に近づける画像処理アルゴリズムです．

実行方法
```
python3 color_transfer. py source_img_path target_img_path save_dir/
```

アルゴリズムの詳細は[qiita][2]に書きました．

# 実行結果
|入力画像|参照画像|実行結果|入力画像と参照画像を逆に|論文中の結果|
|---|---|---|---|---|
|![参照画像](readme_images/fig1.png)|![入力画像](readme_images/fig2.png)|![逆に](readme_images/source=fig1target=fig2.png)|![入力画像と参照画像を逆に](readme_images/source=fig2target=fig1.png)|![論文中の実験結果](readme_images/reference2.png)|
|![入力画像2](readme_images/fig3.png)|![参照画像2](readme_images/fig4.png)|![結果2](readme_images/source=fig3target=fig4.png)|![逆2](readme_images/source=fig4target=fig3.png)|![論文中の実験結果](readme_images/reference3.png)|

実行結果は入力画像の色を参照に近づけた結果です．
イラストに適応した結果です．
|入力画像|参照画像|結果1|結果2|
|---|---|---|---|
|![ef](readme_images/ef.jgp)|![an](readme_images/天使ちゃん.png)|![結果1](readme_images/source=天使ちゃんtarget=ef.png)|![結果2](readme_images/source=eftarget=天使ちゃん.png)


[1]:https://www.cs.tau.ac.il/~turkel/imagepapers/ColorTransfer.pdf

[2]:https://qiita.com/wkiino/items/f4a8f340016951107646


