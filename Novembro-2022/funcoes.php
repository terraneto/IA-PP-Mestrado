<?php
function logs($modulo,$texto){
        $hora = date("H:i:s"); // pega a hora
        $data = date("d-m-Y"); // pega o dia
        /*
            o "a+" abaixo significa:
            - Abre o arquivo para leitura e gravação; 
            - coloca o ponteiro no fim do arquivo. 
            - Se o arquivo não existir, tentar criá-lo.
        */
        $log = fopen("log/".$data.".txt", "a+");
        $escreve = fwrite($log, $modulo." - ".$hora." - ".$texto."\n");// Escreve
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
?>