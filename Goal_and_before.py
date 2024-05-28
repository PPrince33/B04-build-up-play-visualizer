import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable,'-m','pip','install',package])

packages= [
    "streamlit",
    "pandas",
    "mplsoccer",
    "numpy",
    "matplotlib",
    "termcolor",
    "colored"
]

for package in packages:
    try:
        install(package)
    except subprocess.CalledProcessError as e:
        st.write(f"Failed to install {package}: {e}")






import pandas as pd
from mplsoccer import VerticalPitch,Pitch
import matplotlib.pyplot as plt
from termcolor import colored
import streamlit as st
from multiprocessing import freeze_support

def main():
    B04=pd.read_csv("B04.csv")
    B04_vs=pd.read_csv("B04_vs.csv")
    B04=B04.drop(columns='Unnamed: 0')
    B04['goal_id']=''
    B04.loc[B04['shot_outcome']=='Goal','goal_id']='Player-'+B04['player']+' | Time-'+'['+B04['minute'].astype(str)+':'+B04['second'].astype(str)+']'
    st.header("Bayer Leverkusen's Build-Up Play to Goal",divider='red')
    #Dropdown for selection
    list_of_teams=list(B04_vs['possession_team'].unique())
    opponent_team=st.selectbox('Select the opponent team',['',*list_of_teams])
    if opponent_team:
        list_of_match_id=list(B04_vs[B04_vs['possession_team']==opponent_team]['match_id'])
        match_id=st.selectbox('Select the match',['',*list_of_match_id])
        if match_id:
            id_df=B04[B04['match_id']==match_id]
            id_df=id_df.sort_values(by=['minute', 'second'], ascending=True).reset_index(drop=True)
            goal_id_list=list(B04['goal_id'][(B04['match_id']==int(match_id))&(B04['shot_outcome']=='Goal')])
            goal_id = st.selectbox('Select the goal', ['', *goal_id_list])
            if goal_id:
                action_df=id_df[id_df['goal_id']==goal_id]
                index_of_selected_goal = action_df.index[0]
                start_index = max(index_of_selected_goal - 20, 0)
                build_up_df = id_df.loc[start_index:index_of_selected_goal]
                build_up_df=build_up_df[build_up_df['type']!='Pressure']
                pitch = Pitch(pitch_type='statsbomb', pitch_color='#22312b', line_color='#c7d5cc')
                fig, ax = pitch.draw(figsize=(16, 11), constrained_layout=True, tight_layout=False)
                fig.set_facecolor('#22312b')
                text=build_up_df[build_up_df['goal_id']!='']['goal_id'].values
                ax.set_title(f"Build up play of goal {text[0]}",color='White',fontsize=20)
                for i in range(len(build_up_df)):
                    if build_up_df.iloc[i]['type']=='Carry':
                        ax.plot((build_up_df.iloc[i]['location_y_x'],build_up_df.iloc[i]['carry_end_location_x']),
                                (build_up_df.iloc[i]['location_y_y'],build_up_df.iloc[i]['carry_end_location_y']),
                                color='yellow',linestyle='--')
                        
                        mid_x=(build_up_df.iloc[i]['location_y_x']+build_up_df.iloc[i]['carry_end_location_x'])/2
                        mid_y=(build_up_df.iloc[i]['location_y_y']+build_up_df.iloc[i]['carry_end_location_y'])/2
                        ax.text(mid_x, mid_y,f'{i+1}',color='white',fontsize=10)
                        st.write(f"{i+1}){build_up_df.iloc[i]['player']} carried the ball")
                    
                    elif build_up_df.iloc[i]['type']=='Pass':
                        ax.plot((build_up_df.iloc[i]['location_y_x'],build_up_df.iloc[i]['pass_end_location_x']),
                                (build_up_df.iloc[i]['location_y_y'],build_up_df.iloc[i]['pass_end_location_y']),
                                color='green')        
                        mid_x=(build_up_df.iloc[i]['location_y_x']+build_up_df.iloc[i]['pass_end_location_x'])/2
                        mid_y=(build_up_df.iloc[i]['location_y_y']+build_up_df.iloc[i]['pass_end_location_y'])/2
                        ax.text(mid_x, mid_y,f'{i+1}',color='white',fontsize=10)
                        ax.scatter(build_up_df.iloc[i]['location_y_x'],build_up_df.iloc[i]['location_y_y'],color='green',marker='o')
                        st.write(f"{i+1}){build_up_df.iloc[i]['player']} passed the ball")
                        if build_up_df.iloc[i+1]['type']!='Ball Receipt*':
                            ax.scatter(build_up_df.iloc[i]['pass_end_location_x'],build_up_df.iloc[i]['pass_end_location_y'],color='red',marker='x')  
                            st.markdown("<p style='color: red;'>but the pass was unsuccessful</p>", unsafe_allow_html=True)

                    elif build_up_df.iloc[i]['type']=='Shot':
                        if build_up_df.iloc[i]['shot_outcome']=='Goal':            
                            ax.plot((build_up_df.iloc[i]['location_y_x'],build_up_df.iloc[i]['shot_end_location_x']),
                                (build_up_df.iloc[i]['location_y_y'],build_up_df.iloc[i]['shot_end_location_y']),
                                color='purple')
                            ax.scatter(build_up_df.iloc[i]['location_y_x'], build_up_df.iloc[i]['location_y_y'], color='purple',marker='o')
                            mid_x=(build_up_df.iloc[i]['location_y_x']+build_up_df.iloc[i]['shot_end_location_x'])/2
                            mid_y=(build_up_df.iloc[i]['location_y_y']+build_up_df.iloc[i]['shot_end_location_y'])/2
                            ax.text(mid_x, mid_y,f"Goal-{build_up_df.iloc[i]['player']}",color='white',fontsize=5)
                            ax.scatter(build_up_df.iloc[i]['shot_end_location_x'], build_up_df.iloc[i]['shot_end_location_y'], color='orange',marker='p')
                            st.write(f"{i+1}){build_up_df.iloc[i]['player']} scored the goal")
                            
                        else:
                            ax.plot((build_up_df.iloc[i]['location_y_x'],build_up_df.iloc[i]['shot_end_location_x']),
                                (build_up_df.iloc[i]['location_y_y'],build_up_df.iloc[i]['shot_end_location_y']),
                                color='purple')
                            ax.scatter(build_up_df.iloc[i]['location_y_x'], build_up_df.iloc[i]['location_y_y'], color='purple',marker='o')
                            mid_x=(build_up_df.iloc[i]['location_y_x']+build_up_df.iloc[i]['shot_end_location_x'])/2
                            mid_y=(build_up_df.iloc[i]['location_y_y']+build_up_df.iloc[i]['shot_end_location_y'])/2
                            ax.text(mid_x, mid_y,f'{i+1}',color='white',fontsize=10)    
                            st.write(f"{i+1}){build_up_df.iloc[i]['player']} missed the goal")
                    elif build_up_df.iloc[i]['type']=='Ball Receipt*':
                        ax.scatter(build_up_df.iloc[i]['location_y_x'], build_up_df.iloc[i]['location_y_y'], color='green')
                        ax.text(build_up_df.iloc[i]['location_y_x'], build_up_df.iloc[i]['location_y_y'],f'{i+1}',color='white',fontsize=10)
                        st.write(f"{i+1}){build_up_df.iloc[i]['player']} received the ball")
                    elif build_up_df.iloc[i]['type']=='Ball Recovery':
                        ax.scatter(build_up_df.iloc[i]['location_y_x'], build_up_df.iloc[i]['location_y_y'], color='red',marker='>')
                        ax.text(build_up_df.iloc[i]['location_y_x'], build_up_df.iloc[i]['location_y_y'],f'{i+1}',color='white',fontsize=10)
                        st.write(f"{i+1}){build_up_df.iloc[i]['player']} recovered the ball")
                    elif build_up_df.iloc[i]['type']=='Dispossessed':
                        ax.scatter(build_up_df.iloc[i]['location_y_x'], build_up_df.iloc[i]['location_y_y'], color='red',marker='X')
                        ax.text(build_up_df.iloc[i]['location_y_x'], build_up_df.iloc[i]['location_y_y'],f'{i+1}',color='white',fontsize=10)
                        st.write(f"{i+1}){build_up_df.iloc[i]['player']} got dispossessed")
                        
                    else:
                        ax.scatter(build_up_df.iloc[i]['location_y_x'], build_up_df.iloc[i]['location_y_y'], color='orange',marker='*')
                        ax.text(build_up_df.iloc[i]['location_y_x'], build_up_df.iloc[i]['location_y_y'],f'{i+1}',color='white',fontsize=10)
                        st.write(f"{i+1}){build_up_df.iloc[i]['player']} did somthing")
                st.pyplot(fig)
                st.write(build_up_df)
if __name__ == '__main__':

    freeze_support()  # Ensures proper initialization on Windows
    main()  









