using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.IO;

namespace ContainerControl
{
    public partial class ContainerControl : Form
    {
        public ContainerControl()
        {
            InitializeComponent();
        }

        private string ExecuteCommand(string command)
        {
            var processInfo = new ProcessStartInfo("cmd.exe", "/c " + command);
            processInfo.CreateNoWindow = true;
            processInfo.UseShellExecute = false;
            processInfo.RedirectStandardError = true;
            processInfo.RedirectStandardOutput = true;
            int exitCode;
            var process = Process.Start(processInfo);
            process.WaitForExit();

            textBox1.Text += string.Format(@"{0} ", process.StandardError.ReadToEnd());
            string output = string.Format(@"{0}", process.StandardOutput.ReadToEnd());

            exitCode = process.ExitCode;
            process.Close();
            process.Close();
            return output;
        }

        private void button1_Click(object sender, EventArgs e)
        {
            ExecuteCommand(string.Format(@"{0}\Create{1}Image.bat", ExecuteCommand("echo %cd%").Replace("\r\n", ""), listView1.FocusedItem.Text));        
        }

        private string[] getList()
        {
            return Directory.GetDirectories(string.Format(@"{0}\apps", ExecuteCommand("echo %cd%").Replace("\r\n", "")));
        }

        private void ContainerControl_Load(object sender, EventArgs e)
        {
            foreach (string item in getList())
            {
                this.listView1.Items.Add(item.Substring(item.LastIndexOf('\\') + 1));
            }
            listView1.Refresh();
        }

        private void UpdateListButton_Click(object sender, EventArgs e)
        {
            foreach (string item in getList())
            {
                this.listView1.Items.Add(item.Substring(item.LastIndexOf('\\') + 1));
            }
            listView1.Refresh();
        }

        private void RunImageButton_Click(object sender, EventArgs e)
        {
            ExecuteCommand(string.Format(@"{0}\Run{1}Image.bat", ExecuteCommand("echo %cd%").Replace("\r\n", ""), listView1.FocusedItem.Text));
        }

        private void DeleteImageButton_Click(object sender, EventArgs e)
        {
            ExecuteCommand(string.Format(@"{0}\Delete{1}Image.bat", ExecuteCommand("echo %cd%").Replace("\r\n", ""), listView1.FocusedItem.Text));
        }

        private void StopContainerButton_Click(object sender, EventArgs e)
        {
            ExecuteCommand(string.Format(@"{0}\Stop{1}Container.bat", ExecuteCommand("echo %cd%").Replace("\r\n", ""), listView1.FocusedItem.Text));
        }
    }
}
