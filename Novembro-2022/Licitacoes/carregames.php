<?php
 
function logs($texto){
        $hora = date("H:i:s"); // pega a hora
        $data = date("d-m-Y"); // pega o dia
        /*
            o "a+" abaixo significa:
            - Abre o arquivo para leitura e gravação; 
            - coloca o ponteiro no fim do arquivo. 
            - Se o arquivo não existir, tentar criá-lo.
        */
        $log = fopen("log/".$data.".txt", "a+");
        $escreve = fwrite($log, $hora." - ".$texto."\n");// Escreve
        fclose($log); // Fecha o arquivo
    }
    
function curl_get_contents($url)
{
  $ch = curl_init($url);
  curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
  curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 1);
  curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);
  curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 0);
  $data = curl_exec($ch);
  curl_close($ch);
  return $data;
}
$ano=2022;
$hi=date("H:i:s");
logs('Job iniciado '.$hi);
for ($i = 1; $i < 13; $i++) {
    $erro=0;
    $mes = sprintf("%02s",$i);
    $ultimo_dia = date("t", mktime(0,0,0,$mes,'01',$ano));
    $dataini= $ano.'-'.$mes.'-01';
    $datafim= $ano.'-'.$mes.'-'.sprintf("%02s",$ultimo_dia);
    // Initialize a file URL to the variable
    $url = 'http://compras.dados.gov.br/licitacoes/v1/licitacoes.json?item_material_classificacao=7010&data_publicacao_min='.$dataini.'&data_publicacao_max='.$datafim;
    $file_name = basename('licitacoes'.$ano.'-'.$mes.'.json');
    logs($file_name);
    while($erro<5){
       if(file_put_contents( $file_name,curl_get_contents($url))) {
          logs("File downloaded successfully");
          break;
       }
       else {
          $erro=$erro+1;
          logs("File downloading failed. Erro=".$erro);
       }
    }
}
logs('Job '.$hi.'concluído '.date("H:i:s"));
?>