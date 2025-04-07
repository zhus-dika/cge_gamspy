import pandas as pd
import numpy as np
import os


def aggregate_industries(filepath, sheet_name='final', n_industries=10):
    # Чтение файла
    df = pd.read_excel(filepath, sheet_name=sheet_name, index_col=0)

    # Количество начальных индустрий
    old_industries = df.index[:34]  # первые 34 строки и столбца — индустрии
    other_rows = df.index[34:]
    other_cols = df.columns[34:]

    # Делим 34 индустрии на группы для агрегации
    indices = list(range(34))
    split_indices = np.array_split(indices, n_industries)
    new_names = [f'Ind_{i + 1}' for i in range(n_industries)]

    # Агрегация квадратной части (индустрии на индустрии)
    sam_agg = pd.DataFrame(index=new_names, columns=new_names)

    for i, row_group in enumerate(split_indices):
        for j, col_group in enumerate(split_indices):
            sam_agg.iloc[i, j] = df.iloc[row_group, col_group].sum().sum()

    # Агрегация столбцов (индустрии vs остальные колонки)
    agg_cols = pd.DataFrame(index=df.index)

    for idx, group in enumerate(split_indices):
        agg_cols[new_names[idx]] = df.iloc[:, group].sum(axis=1)

    # Агрегация строк (индустрии vs остальные строки)
    agg_rows = pd.DataFrame(index=new_names, columns=df.columns)

    for idx, group in enumerate(split_indices):
        agg_rows.loc[new_names[idx]] = df.iloc[group, :].sum(axis=0)

    # Собираем финальную таблицу
    top = pd.concat([sam_agg, agg_rows.loc[:, other_cols]], axis=1)
    bottom = pd.concat([agg_cols.loc[other_rows, new_names], df.loc[other_rows, other_cols]], axis=1)

    final_df = pd.concat([top, bottom], axis=0)

    return final_df


def main():
    current_path = os.path.abspath(os.path.dirname(__file__))
    sam_path = os.path.join(current_path, "data", "databank_2017_type1_common_HOH.xlsx")
    output_path = os.path.join(current_path, "data", 'aggregated_sam.xlsx')  # куда сохранить результат
    n_industries = 3  # сколько индустрий хотим оставить

    agg_df = aggregate_industries(sam_path, sheet_name='final', n_industries=n_industries)

    # Сохраняем в Excel
    agg_df.to_excel(output_path)
    print(f'Готово! Файл сохранён в {output_path}')


if __name__ == '__main__':
    main()
