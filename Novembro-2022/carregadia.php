<?php
 
require 'funcoes.php';

$ano=2022;
$hi=date("H:i:s");
logs('CarregaDia','Job iniciado '.$hi);
for ($i = 1; $i < 13; $i++) {
    $mes = sprintf("%02s",$i);
    $ultimo_dia = date("t", mktime(0,0,0,$mes,'01',$ano));
    for ($d = 1; $d <= $ultimo_dia; $d++){
       $erro=0;
       $datafim= $ano.'-'.$mes.'-'.sprintf("%02s",$d);
       $url = 'http://compras.dados.gov.br/licitacoes/v1/licitacoes.json?item_material_classificacao=7010&data_publicacao='.$datafim;
       $file_name = basename('licitacoes'.$datafim.'.json');
       logs('CarregaDia',$file_name);
       baixar_arquivo($url,$file_name);
    }
}
logs('CarregaDia','Job '.$hi.'concluído '.date("H:i:s"));
?>