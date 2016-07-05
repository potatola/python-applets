using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Security.Cryptography;
using System.Text;
using System.Threading.Tasks;
using IronPython.Hosting;
using Microsoft.Scripting.Hosting;
using System.Threading;

namespace ConsoleApplication1
{
    class Program
    {
        static void Main(string[] args)
        {
            StreamWriter sw = File.AppendText("ExcuteLog.txt");
            DateTime dt = new DateTime();
            dt = System.DateTime.Now;
            string strFu = dt.ToString("yyyy-MM-dd HH:mm:ss");
            sw.WriteLine("Run at: " + strFu);
            sw.Flush();
            sw.Close();

            ScriptRuntime pyRunTime = Python.CreateRuntime();
            dynamic obj = pyRunTime.UseFile("web.py");

            Console.WriteLine("Try fetch data from the server...");
            string webData = null;
            bool fetchFinish = false;
            int try_count = 0;
            while (!fetchFinish)
            {
                try
                {
                    webData = obj.get_web_data();
                    fetchFinish = true;
                }
                catch
                {
                    try_count++;
                    if (try_count >= 10)
                    {
                        Console.WriteLine("Fetch failed! Exit.");
                        return;
                    }
                    Console.WriteLine("Fetch failed! Retry in 1s...");
                    Thread.Sleep(1000);
                }
            }

            Console.WriteLine("Fetch data finished. Try decrypting...");

            //decrypte
            string key = "qjkHuIy9D/9i=";
            string salt = "Mi9l/+7Zujhy12se6Yjy111A";

            string decWebData = DecryptAES(webData, key, salt);
            //Console.WriteLine(decWebData);

            //StreamReader sr = new StreamReader("C:\\Users\\gengy\\Documents\\Visual Studio 2012\\Projects\\ConsoleApplication1\\ConsoleApplication1\\bin\\Debug\\post_res.txt", Encoding.Default);
            //string input = sr.ReadLine();
            //string decWebData = DecryptAES(input, key, salt);

            Console.WriteLine("Decrypt finished. Try parsing...");
            obj.parse_table(decWebData);

            Console.WriteLine("All finished.");
        }

        /// <summary>
        /// hmacSha1算法加密（生成长度40）
        /// </summary>
        /// <param name="signatureString">加密明文</param>
        /// <param name="secretKey">加密密钥</param>
        /// <param name="raw_output">是否输出原始编码</param>
        /// <returns></returns>
        public static object hmacSha1(string signatureString, string secretKey, bool raw_output = false)
        {
            var enc = Encoding.UTF8;
            HMACSHA1 hmac = new HMACSHA1(enc.GetBytes(secretKey));
            hmac.Initialize();

            byte[] buffer = enc.GetBytes(signatureString);
            if (raw_output)
            {
                return hmac.ComputeHash(buffer);
            }
            else
            {
                return BitConverter.ToString(hmac.ComputeHash(buffer)).Replace("-", "").ToLower();
            }
        }

        /// <summary>
        /// 使用AES加密字符串
        /// </summary>
        /// <param name="encryptString">待加密字符串</param>
        /// <param name="encryptKey">加密密匙</param>
        /// <param name="salt">盐</param>
        /// <returns>加密结果，加密失败则返回源串</returns>
        public static string EncryptAES(string encryptString, string encryptKey, string salt)
        {
            AesManaged aes = null;
            MemoryStream ms = null;
            CryptoStream cs = null;

            string str = null;

            try
            {
                Rfc2898DeriveBytes rfc2898 = new Rfc2898DeriveBytes(encryptKey, Encoding.UTF8.GetBytes(salt));

                aes = new AesManaged();
                aes.Key = rfc2898.GetBytes(aes.KeySize / 8);
                aes.IV = rfc2898.GetBytes(aes.BlockSize / 8);

                ms = new MemoryStream();
                cs = new CryptoStream(ms, aes.CreateEncryptor(), CryptoStreamMode.Write);

                byte[] data = Encoding.UTF8.GetBytes(encryptString);
                cs.Write(data, 0, data.Length);
                cs.FlushFinalBlock();

                str = Convert.ToBase64String(ms.ToArray());
            }
            catch
            {
                str = encryptString;
            }
            finally
            {
                if (cs != null)
                    cs.Close();

                if (ms != null)
                    ms.Close();

                if (aes != null)
                    aes.Clear();
            }

            return str;
        }

        /// <summary>
        /// 使用AES解密字符串
        /// </summary>
        /// <param name="decryptString">待解密字符串</param>
        /// <param name="decryptKey">解密密匙</param>
        /// <param name="salt">盐</param>
        /// <returns>解密结果，解谜失败则返回源串</returns>
        public static string DecryptAES(string decryptString, string decryptKey, string salt)
        {
            AesManaged aes = null;
            MemoryStream ms = null;
            CryptoStream cs = null;

            string str = null;

            try
            {
                Rfc2898DeriveBytes rfc2898 = new Rfc2898DeriveBytes(decryptKey, Encoding.UTF8.GetBytes(salt));

                aes = new AesManaged();
                aes.Key = rfc2898.GetBytes(aes.KeySize / 8);
                aes.IV = rfc2898.GetBytes(aes.BlockSize / 8);

                ms = new MemoryStream();
                cs = new CryptoStream(ms, aes.CreateDecryptor(), CryptoStreamMode.Write);

                byte[] data = Convert.FromBase64String(decryptString);
                cs.Write(data, 0, data.Length);
                cs.FlushFinalBlock();

                str = Encoding.UTF8.GetString(ms.ToArray(), 0, ms.ToArray().Length);
            }
            catch
            {
                str = decryptString;
            }
            finally
            {
                if (cs != null)
                    cs.Close();

                if (ms != null)
                    ms.Close();

                if (aes != null)
                    aes.Clear();
            }

            return str;
        }

    }
}
