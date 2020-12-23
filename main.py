import names
import math
import pandas as pd
import altair as alt
import data


def chart_matrix(df):
    df['Score'] = df['Score'].apply(str)

    brush = alt.selection_interval()

    ability_chart = variable_rank_chart(df, 'Ability', brush,
                                        ["Non-magical", "Magic-aware", "Magic-user", "Talented", "Gifted"])

    personality_chart = variable_rank_chart(df, 'Personality', brush,
                                            ["Undesirable", "Suspect", "As Expected", "Good Fit", "Excellent Fit"])

    achievements_chart = variable_rank_chart(df, 'Achievements', brush,
                                             ["None", "As Expected", "Exceeding", "Extraordinary"])

    family_chart = variable_rank_chart(df, 'Family Fame', brush,
                                       ["Unknown", "Known", "Established", "Prominent", "Illustrious", "Legendary"])

    return ability_chart | personality_chart | achievements_chart | family_chart


def variable_rank_chart(df, variable, brush, sort):
    chart = alt.Chart(df).mark_circle().encode(
        alt.X(variable, type='ordinal', sort=sort),
        alt.Y('Rank:Q', sort=None),
        color=alt.condition(brush, 'Status:O', alt.value('lightgray'))
    ).add_selection(
        brush
    ).properties(
        width=150,
        height=250
    )

    return chart


def chart_score(df):
    df['STATUS_ORD'] = df.apply(
        lambda row: 2 if row['Status'] == 'admitted' else (1 if row['Status'] == 'wait-listed' else 0), axis=1)
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('Score:O', sort=None),
        y=alt.Y('Frequency', title='Number of Students'),
        color=alt.Color('Status', scale=alt.Scale(
            domain=['admitted', 'wait-listed', 'rejected'],
            range=['green', 'cyan', 'orange'])),
        order=alt.Order(
            'STATUS_ORD'))

    return chart


def group_by_scores(df):
    tidied = df.drop(['Family Fame', 'Ability', 'Achievements', 'Personality', 'Rank'], axis=1)
    grouped = tidied.groupby(['Score', 'Status']).size()
    grouped = grouped.reset_index()
    grouped.columns = ['Score', 'Status', 'Frequency']
    grouped['Score'] = grouped['Score'].apply(str)
    return grouped


def convert_to_df(students):
    index = 0
    dictionary_form = {}
    for student in students:
        dictionary_form[index] = student.get_attributes()
        index += 1
    df = pd.DataFrame(data=dictionary_form).transpose()
    df.columns = ['Name', 'Family Fame', 'Ability', 'Achievements', 'Personality', 'Score', 'Rank', 'Status']
    return df


def admissions(to_admit, students):
    for student in students:
        if student.rank <= to_admit:
            student.status = 'admitted'
        elif student.rank <= to_admit + data.waitlist_size:
            student.status = 'wait-listed'
        else:
            student.status = 'rejected'


def rank(students):
    ranking = sorted(students, key=lambda x: x.score, reverse=True)
    for i in range(len(ranking)):
        ranking[i].rank = i


def score(student):
    raw_score = sum([data.familyScoring[student.familyFame]
                   , data.abilityScoring[student.ability]
                   , data.achievementsScoring[student.achievements]
                   , data.personalityScoring[student.personality]])
    return raw_score if raw_score == raw_score else -math.inf


def get_students(n):
    return list(map(lambda _: Student(), [0]*n))


def student_gen():
    while True:
        yield Student()


class Student:
    def __init__(self):
        self.name = names.get_full_name()
        self.familyFame = data.familyGen.get_a_value()
        self.ability = data.abilityGen.get_a_value()
        self.achievements = data.achievementsGen.get_a_value()
        self.personality = data.personalityGen.get_a_value()
        self.score = score(self)
        self.rank = None
        self.status = 'Pending'

    def get_attributes(self):
        return [self.name, self.familyFame, self.ability, self.achievements
               ,self.personality, self.score, self.rank, self.status]
    
    def __repr__(self):
        return (f"\nName: {self.name}, Family Fame: {self.familyFame}\n" +
                f"Ability: {self.ability}, Achievements: {self.achievements}\n" +
                f"Personality: {self.personality}\n" +
                f"SCORE = {self.score}\n")


if __name__ == "__main__":
    students = get_students(data.applications)
    rank(students)
    admissions(data.intake_size, students)
    df = convert_to_df(students)
    grouped = group_by_scores(df)
    score_bars = chart_score(grouped)
    variable_mat = chart_matrix(df)

    (score_bars & variable_mat).show()
