# ADM-HW2

This repository includes the solutions of Homework 2 from the Group 21:

<div style="float: left;">
    <table>
        <tr>
            <th>Student</th>
            <th>Matricola</th>
            <th>E-Mail</th>
        </tr>
        <tr>
            <td>Santiago Vessi</td>
            <td>1958879</td>
            <td>vessi.1958879@studenti.uniroma1.it</td>
        </tr>
        <tr>
            <td>Jose Angel Mola</td>
            <td>2116134</td>
            <td>molaaudi.2116134@studenti.uniroma1.it</td>
        </tr>
        <tr>
            <td></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td>André Leibrant</td>
            <td>2085698</td>
            <td>leibrant.2085698@studenti.uniroma1.it</td>
        </tr>
    </table>
</div>

The main notebook is `ADM-HW2.ipynb` which reads the module `functions.py`. The image `ERD.png` pictures the structure of the database we created for our analysis.

The shell scripts for the Command Line Question are `commandline_original.sh` and `commandline_LLM.sh`. For this execute the scripts from the same folder the `series.json` is stored!

The Python script which was uploaded to the AWS EC2 instance and executed from there is `awsq_script.py`.

**Note:** The notebook `ADM-HW2.ipynb` creates a local database `tables.db` (approximately 7GB) using the `SQLite3` package in the same folder as the notebook. If the file already exists only a connection to the database is being established.
