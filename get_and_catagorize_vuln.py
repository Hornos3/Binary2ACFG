# coding=utf-8
import os
import shutil
import sys
from pymysql import *

version_dict = {'0.9.7': 1, '0.9.8': 2, '1.0.0': 3, '1.0.1': 4, '1.0.2': 5, '1.1.0': 6, '1.1.1': 7}

def connection(database_key):
    mysql = {'host': '', 'port': 3306, 'user': 'root', 'passwd': '', 'db': '', 'charset': 'utf8'}
    if database_key == 'test':
        mysql['host'] = 'localhost'
        mysql['passwd'] = '20030509@Lhy'
        mysql['db'] = 'features'
    return mysql

def collect_idaFiles():         # 将ida文件转移到一个文件夹中
    if not os.path.isdir('.\\ida_files'):
        os.mkdir('.\\ida_files')
    for root, dir, files in os.walk('.\\firmware'):
        for f in files:
            if f.split('.')[-1] == 'ida':
                shutil.copy(root + '\\' + f, '.\\ida_files\\' + f)

if __name__ == '__main__':
    conn = connect(**connection("test"))
    cursor = conn.cursor()
    # selected_version = sys.argv[1]      # vulnerability version needed to search
    # if selected_version not in version_dict.keys():
    #     print('version error')
    #     exit(1)
    # search_str = "select * from vuln_function where version like '%<{x}'"

    cursor.execute("select * from vuln_function where version like '%<1.1.1%' and version not like '%1.1.0%';")
    list = cursor.fetchall()
    filelist1 = []
    for ele in list:
        if [ele[1], ele[2].replace(".c", "")] not in filelist1:
            filelist1.append([ele[1], ele[2].replace(".c", "")])

    # cursor.execute("select * from vuln_function where version not like '%0.9.8%' and version like '%1.0.1%';")
    # list = cursor.fetchall()
    # filelist2 = []
    # for ele in list:
    #     if [ele[1], ele[2].replace(".c", "")] not in filelist2:
    #         filelist2.append([ele[1], ele[2].replace(".c", "")])

    for func in filelist1:
        # if func not in filelist2:
        # print(func)
        try:
            print(func)
            shutil.copy('.\\selected_files_1.1.1a\\' + func[1], func[1])
            os.system('python main.py ' + func[1] + ' C:\\Users\\win7_lihongyuan\\Desktop\\IDA_Pro_v6.8\\idaq64.exe ' + func[0] +
                      ' openssl 1.1.1a mips')
        except Exception:
            pass

    collect_idaFiles()

'''
[u'ssl_scan_clienthello_tlsext', u't1_lib']
[u'ssl_parse_clienthello_tlsext', u't1_lib']
[u'X509_NAME_oneline', u'x509_obj']
[u'asn1_d2i_read_bio', u'a_d2i_fp']
[u'asn1_ex_i2c', u'tasn_enc']
[u'asn1_ex_c2i', u'tasn_dec']
[u'ASN1_TYPE_cmp', u'a_type']
[u'aesni_cbc_hmac_sha256_cipher', u'e_aes_cbc_hmac_sha256']
[u'aesni_cbc_hmac_sha1_cipher', u'e_aes_cbc_hmac_sha1']
[u'EVP_EncryptUpdate', u'evp_enc']
[u'EVP_EncodeUpdate', u'encode']
[u'cmd_Protocol', u'ssl_conf']
[u'_dopr', u'b_print']
[u'BIO_vprintf', u'b_print']
[u'doapr_outch', u'b_print']
[u'fmtint', u'b_print']
[u'fmtfp', u'b_print']
[u'fmtstr', u'b_print']
[u'BIO_vsnprintf', u'b_print']
[u'ssl_srp_server_param_cb', u's_server']
[u'www_body', u's_server']
[u'init_ssl_connection', u's_server']
[u'sv_body', u's_server']
[u'SRP_VBASE_get_by_user', u'srp_vfy']
[u'rev_body', u's_server']
[u'BN_hex2bn', u'bn_print']
[u'BN_dec2bn', u'bn_print']
[u'dsa_priv_decode', u'dsa_ameth']
[u'BN_mod_exp_mont_consttime', u'bn_exp']
[u'MOD_EXP_CTIME_COPY_FROM_PREBUF', u'bn_exp']
[u'MOD_EXP_CTIME_COPY_TO_PREBUF', u'bn_exp']
[u'get_client_master_key', u's2_srvr']
[u'get_client_hello', u's2_srvr']
[u'rsa_pss_decode', u'rsa_ameth']
[u'rsa_mgf1_decode', u'rsa_ameth']
[u'X509_verify_cert', u'x509_vfy']
[u'test_alt_chains_cert_forgery', u'verify_extra_test']
[u'dtls1_read_bytes', u'd1_pkt']
[u'dtls1_get_record', u'd1_pkt']
[u'dtls1_process_buffered_records', u'd1_pkt']
[u'dtls1_buffer_record', u'd1_pkt']
[u'dtls1_process_record', u'd1_pkt']
[u'ssl3_get_cert_verify', u's3_srvr']
[u'ssl3_get_server_hello', u's3_clnt']
[u'ssl_scan_serverhello_tlsext', u't1_lib']
[u'ssl_add_serverhello_tlsext', u't1_lib']
[u'ssl_add_clienthello_tlsext', u't1_lib']
[u'ssl_parse_clienthello_use_srtp_ext', u'd1_srtp']
[u'ssl_parse_serverhello_tlsext', u't1_lib']
[u'ssl23_get_client_hello', u's23_srvr']
[u'ssl_set_client_disabled', u't1_lib']
[u'tls1_process_heartbeat', u't1_lib']
[u'dtls1_process_heartbeat', u'd1_both']
[u'tls1_change_cipher_state', u't1_enc']
[u'dtls1_hm_fragment_free', u'd1_both']
[u'ssl3_get_server_certificate', u's3_clnt']
[u'ssl3_get_certificate_request', u's3_clnt']
[u'ssl3_get_client_certificate', u's3_srvr']
'''