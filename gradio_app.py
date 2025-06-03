import gradio as gr
from theme_classifier import ThemeClassifier
from Character_network import NameEntityRecongnizer,CharacterNetworkGenerator
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

def get_character_network(subtitles_path,ner_path):
    ner= NameEntityRecongnizer()
    ner_df = ner.get_ners(subtitles_path,ner_path)

    character_network_gen = CharacterNetworkGenerator()
    relationship_df = character_network_gen.generate_character_network(ner_df)

    html = character_network_gen.draw_network_graph(relationship_df)
    return html

def main():
    with gr.Blocks() as iface:
        #this is for theme classificaton
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

        #this is for character network

        with gr.Row():
            with gr.Column():
                gr.HTML("<h1> Character Network(Ner and graph) </h1>")
                with gr.Row():
                    with gr.Column():
                        network_html = gr.HTML()
                    with gr.Column():
                        
                        network_subtitles_path = gr.Textbox(label = "Subtitles or scripts path")
                        ner_save_path = gr.Textbox(label= "NERs Save path")
                        get_network_graph_button = gr.Button("Get Character Network")
             
                        get_network_graph_button.click(get_character_network,inputs=[network_subtitles_path,ner_save_path],outputs= [network_html])

    iface.launch()




if __name__ == '__main__':
    main()