import gradio as gr
from theme_classifier import ThemeClassifier
def get_themes(theme_list_str,subtitle_path,save_path):
    theme_list = theme_list_str.split(',')
    theme_classifier = ThemeClassifier(theme_list)
    
    output_df = theme_classifier.get_themes(subtitle_path,save_path)
    theme_list = [theme for theme in theme_list if theme != "dialogue"]
    ouput_df = output_df[theme_list]

    output_df =output_df[theme_list].sum().reset_index()
    output_df.columns = ['Theme','Score']

    output_chart = gr.BarPlot(output_df,
                              x = "Score",
                              y = "Theme",
                              title="Serie Themes",
                              tooltip=["Theme","Score"],
                             
                              width = 500,
                              height = 260
                              )
    return output_chart

def main():
    with gr.Blocks() as iface:
        with gr.Row():
            with gr.Column():
                gr.HTML("<h1> Theme Classification (Zero Shot Classifier) </h1>")
                with gr.Row():
                    with gr.Column():
                        plot = gr.BarPlot()
                    with gr.Column():
                        theme_list = gr.Textbox(label= "Themes")
                        subtitles_path = gr.Textbox(label = "Subtitles or scripts path")
                        save_path = gr.Textbox(label= "Save path")
                        get_themes_bt = gr.Button("Get Themes")
                        get_themes_bt.click(get_themes,inputs=[theme_list,subtitles_path,save_path],outputs= [plot])


    iface.launch()




if __name__ == '__main__':
    main()