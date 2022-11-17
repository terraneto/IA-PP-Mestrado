<?php
 
require 'funcoes.php';

$ano=2022;
$hi=date("H:i:s");
logs('CarregaMes','Job iniciado '.$hi);
for ($i = 1; $i < 13; $i++) {
    $erro=0;
    $mes = sprintf("%02s",$i);
    $ultimo_dia = date("t", mktime(0,0,0,$mes,'01',$ano));
    $dataini= $ano.'-'.$mes.'-01';
    $datafim= $ano.'-'.$mes.'-'.sprintf("%02s",$ultimo_dia);
    $url = 'http://compras.dados.gov.br/licitacoes/v1/licitacoes.json?item_material_classificacao=7010&data_publicacao_min='.$dataini.'&data_publicacao_max='.$datafim;
    $file_name = basename('licitacoes'.$ano.'-'.$mes.'.json');
    logs('CarregaMes',$file_name);
    baixar_arquivo($url,$file_name);
}
logs('CarregaMes','Job '.$hi.'concluído '.date("H:i:s"));
?>