namespace ContainerControl
{
    partial class ContainerControl
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.CreateImageButton = new System.Windows.Forms.Button();
            this.RunImageButton = new System.Windows.Forms.Button();
            this.UpdateListButton = new System.Windows.Forms.Button();
            this.StopConainerButton = new System.Windows.Forms.Button();
            this.textBox1 = new System.Windows.Forms.TextBox();
            this.listView1 = new System.Windows.Forms.ListView();
            this.DeleteImageButton = new System.Windows.Forms.Button();
            this.label1 = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.SuspendLayout();
            // 
            // CreateImageButton
            // 
            this.CreateImageButton.Location = new System.Drawing.Point(12, 41);
            this.CreateImageButton.Name = "CreateImageButton";
            this.CreateImageButton.Size = new System.Drawing.Size(88, 23);
            this.CreateImageButton.TabIndex = 0;
            this.CreateImageButton.Text = "CreateImage";
            this.CreateImageButton.UseVisualStyleBackColor = true;
            this.CreateImageButton.Click += new System.EventHandler(this.button1_Click);
            // 
            // RunImageButton
            // 
            this.RunImageButton.Location = new System.Drawing.Point(12, 70);
            this.RunImageButton.Name = "RunImageButton";
            this.RunImageButton.Size = new System.Drawing.Size(88, 23);
            this.RunImageButton.TabIndex = 1;
            this.RunImageButton.Text = "RunImage";
            this.RunImageButton.UseVisualStyleBackColor = true;
            this.RunImageButton.Click += new System.EventHandler(this.RunImageButton_Click);
            // 
            // UpdateListButton
            // 
            this.UpdateListButton.Location = new System.Drawing.Point(12, 12);
            this.UpdateListButton.Name = "UpdateListButton";
            this.UpdateListButton.Size = new System.Drawing.Size(88, 23);
            this.UpdateListButton.TabIndex = 2;
            this.UpdateListButton.Text = "UpdateList";
            this.UpdateListButton.UseVisualStyleBackColor = true;
            this.UpdateListButton.Click += new System.EventHandler(this.UpdateListButton_Click);
            // 
            // StopConainerButton
            // 
            this.StopConainerButton.Location = new System.Drawing.Point(12, 99);
            this.StopConainerButton.Name = "StopConainerButton";
            this.StopConainerButton.Size = new System.Drawing.Size(88, 23);
            this.StopConainerButton.TabIndex = 3;
            this.StopConainerButton.Text = "StopConainer";
            this.StopConainerButton.UseVisualStyleBackColor = true;
            this.StopConainerButton.Click += new System.EventHandler(this.StopContainerButton_Click);
            // 
            // textBox1
            // 
            this.textBox1.Location = new System.Drawing.Point(12, 178);
            this.textBox1.Multiline = true;
            this.textBox1.Name = "textBox1";
            this.textBox1.Size = new System.Drawing.Size(419, 78);
            this.textBox1.TabIndex = 4;
            // 
            // listView1
            // 
            this.listView1.Location = new System.Drawing.Point(106, 33);
            this.listView1.Name = "listView1";
            this.listView1.Size = new System.Drawing.Size(325, 139);
            this.listView1.TabIndex = 5;
            this.listView1.UseCompatibleStateImageBehavior = false;
            // 
            // DeleteImageButton
            // 
            this.DeleteImageButton.Location = new System.Drawing.Point(12, 128);
            this.DeleteImageButton.Name = "DeleteImageButton";
            this.DeleteImageButton.Size = new System.Drawing.Size(88, 23);
            this.DeleteImageButton.TabIndex = 6;
            this.DeleteImageButton.Text = "DeleteImage";
            this.DeleteImageButton.UseVisualStyleBackColor = true;
            this.DeleteImageButton.Click += new System.EventHandler(this.DeleteImageButton_Click);
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(12, 159);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(34, 13);
            this.label1.TabIndex = 7;
            this.label1.Text = "Errors";
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(106, 17);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(59, 13);
            this.label2.TabIndex = 8;
            this.label2.Text = "ServiceList";
            // 
            // ContainerControl
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(443, 268);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.DeleteImageButton);
            this.Controls.Add(this.listView1);
            this.Controls.Add(this.textBox1);
            this.Controls.Add(this.StopConainerButton);
            this.Controls.Add(this.UpdateListButton);
            this.Controls.Add(this.RunImageButton);
            this.Controls.Add(this.CreateImageButton);
            this.Name = "ContainerControl";
            this.Text = "ContainerControl";
            this.Load += new System.EventHandler(this.ContainerControl_Load);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Button CreateImageButton;
        private System.Windows.Forms.Button RunImageButton;
        private System.Windows.Forms.Button UpdateListButton;
        private System.Windows.Forms.Button StopConainerButton;
        private System.Windows.Forms.TextBox textBox1;
        private System.Windows.Forms.ListView listView1;
        private System.Windows.Forms.Button DeleteImageButton;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label label2;
    }
}