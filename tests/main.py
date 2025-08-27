import random
import time
from collections import deque
from sklearn.linear_model import LinearRegression

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER


class BackendDeveloperSimulator:
    def __init__(self):
        self.skills = {
            'python': 1, 'sql': 1, 'api_design': 1,
            'debugging': 1, 'testing': 1, 'deployment': 1,
            'docker': 1, 'aws': 1, 'ml': 1, 'security': 1,
            'kubernetes': 1, 'redis': 1, 'nginx': 1, 'ci_cd': 1,
            'graphql': 1, 'microservices': 1, 'serverless': 1,
            'elasticsearch': 1, 'kafka': 1, 'grpc': 1
        }
        self.energy = 200
        self.max_energy = 200
        self.money = 1500
        self.reputation = 0
        self.level = 1
        self.max_level = 30
        self.xp = 0
        self.projects_completed = 0
        self.bugs_fixed = 0
        self.current_projects = deque()
        self.max_concurrent_projects = 1
        self.project_queue = deque()
        self.max_queue_size = 5
        self.ml_model = LinearRegression()

        self.message_log = []
        self.colors = {
            'text': '#C8DCFF',
            'highlight': '#64C8FF',
            'success': '#64FF96',
            'error': '#FF6464',
            'warning': '#FFC864'
        }

        for _ in range(3):
            self.project_queue.append(self.generate_project())

    def get_learn_cost(self):
        base_cost = 300
        return int(max(100, base_cost - (self.reputation // 10) * 20))

    def get_research_cost(self):
        base_cost = 200
        return int(max(50, base_cost - (self.reputation // 15) * 15))

    def get_mentor_cost(self):
        base_cost = 50
        return int(max(10, base_cost - (self.reputation // 20) * 5))

    def get_deploy_cost(self):
        base_cost = 100
        return int(max(25, base_cost - (self.reputation // 25) * 10))

    def get_scale_cost(self):
        base_cost = 150
        return int(max(40, base_cost - (self.reputation // 30) * 15))

    def get_migrate_cost(self):
        base_cost = 120
        return int(max(30, base_cost - (self.reputation // 35) * 12))

    def get_audit_cost(self):
        base_cost = 180
        return int(max(45, base_cost - (self.reputation // 40) * 18))

    def get_reputation_bonus(self):
        return 1 + (self.reputation // 50) * 0.1

    def get_skill_bonus_multiplier(self):
        return 1 + (self.level // 5) * 0.2

    def generate_project(self):
        project_types = [
            {'name': 'Простой CRUD API', 'difficulty': 1, 'reward': 200, 'time': 2},
            {'name': 'База данных пользователей', 'difficulty': 2, 'reward': 400, 'time': 3},
            {'name': 'Микросервис аутентификации', 'difficulty': 3, 'reward': 800, 'time': 5},
            {'name': 'Система кэширования Redis', 'difficulty': 4, 'reward': 1500, 'time': 8},
            {'name': 'ML рекомендательная система', 'difficulty': 5, 'reward': 3000, 'time': 12},
        ]

        max_difficulty = min(10, 3 + self.level // 2)
        available_projects = [p for p in project_types if p['difficulty'] <= max_difficulty]

        if not available_projects:
            available_projects = project_types[:3]

        return random.choice(available_projects)

    def add_message(self, message, color_type='text'):
        color = self.colors[color_type]
        self.message_log.append({'text': message, 'color': color})
        if len(self.message_log) > 20:
            self.message_log.pop(0)

    def get_bugs_text(self, bugs_count):
        if bugs_count == 1:
            return "1 баг исправлен"
        elif 2 <= bugs_count <= 4:
            return f"{bugs_count} бага исправлено"
        else:
            return f"{bugs_count} багов исправлено"

    def start_project(self):
        if len(self.current_projects) >= self.max_concurrent_projects:
            return f"Максимум {self.max_concurrent_projects} активных проекта!", 'warning'

        if not self.project_queue:
            return "Нет доступных проектов!", 'warning'

        if self.energy < 25:
            return "Слишком устал!", 'warning'

        project = self.project_queue.popleft()
        self.current_projects.append(project)
        self.energy -= 25
        return f"Начал проект: {project['name']} (-25 энергии)", 'success'

    def complete_project(self):
        if not self.current_projects:
            return "Нет активных проектов!", 'warning'

        project = self.current_projects[0]

        if self.energy < 15:
            return "Слишком устал!", 'warning'

        success_chance = self.calculate_success_chance()
        if random.random() < success_chance:
            reward = project['reward']
            self.money += reward
            self.xp += project['difficulty'] * 10
            self.projects_completed += 1
            self.reputation += project['difficulty']
            self.energy -= 15
            result = f"Проект '{project['name']}' завершен! +{reward} денег, +{project['difficulty'] * 10} опыта"
        else:
            self.energy -= 10
            result = f"Проект '{project['name']}' провален! (-10 энергии)"
            self.project_queue.appendleft(project)

        self.current_projects.popleft()
        return result, 'success' if 'успешно' in result else 'error'

    def calculate_success_chance(self):
        return min(0.98, 0.3 + sum(self.skills.values()) / 180 + min(0.2, self.reputation / 500))

    def fix_bugs(self):
        if self.energy < 15:
            return "Слишком устал!", 'warning'

        bugs = random.randint(1, 5)
        reward = bugs * 50
        self.bugs_fixed += bugs
        self.money += reward
        self.xp += bugs * 5
        self.energy -= 15
        self.skills['debugging'] += 0.1

        return f"Исправлено {bugs} багов! +{reward} денег, +{bugs * 5} опыта", 'success'

    def learn_skill(self):
        cost = self.get_learn_cost()
        if self.money < cost:
            return f"Недостаточно денег! ({cost})", 'warning'

        if self.energy < 20:
            return "Слишком устал!", 'warning'

        skill = random.choice(list(self.skills.keys()))
        improvement = random.uniform(0.2, 0.5)
        self.skills[skill] += improvement
        self.money -= cost
        self.energy -= 20

        return f"Прокачал {skill}: +{improvement:.1f} (-{cost} денег)", 'success'

    def rest(self):
        energy_gain = random.randint(25, 45)
        self.energy = min(self.max_energy, self.energy + energy_gain)
        return f"Отдохнул: +{energy_gain} энергии", 'success'

    def check_level_up(self):
        if self.xp >= self.level * 100:
            old_level = self.level
            self.level += 1
            self.xp = 0

            if self.level % 5 == 0:
                self.max_concurrent_projects += 1
                self.max_queue_size += 2
                self.max_energy += 20
                bonus_msg = f", +1 к макс. проектам, +2 к очереди, +20 энергии"
            else:
                self.max_energy += 10
                bonus_msg = f", +10 энергии"

            self.energy = self.max_energy

            if self.level > self.max_level:
                self.level = self.max_level
                return f"Максимальный уровень {self.max_level}!", 'highlight'

            return f"Уровень повышен! {old_level} -> {self.level}{bonus_msg}", 'highlight'
        return None


class BackendSimulatorApp(toga.App):
    def startup(self):
        self.game = BackendDeveloperSimulator()
        
        # Основной контейнер
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=10, flex=1))
        
        # Заголовок
        header = toga.Label(
            'Симулятор Бэкенд-Разработчика',
            style=Pack(font_size=20, font_weight='bold', padding_bottom=10, text_align=CENTER)
        )
        
        # Панель статуса
        status_box = toga.Box(style=Pack(direction=ROW, padding_bottom=10))
        self.status_labels = {}
        
        status_data = [
            ('level', 'Уровень'), ('energy', 'Энергия'),
            ('money', 'Деньги'), ('reputation', 'Репутация')
        ]
        
        for key, text in status_data:
            status_item = toga.Box(style=Pack(direction=COLUMN, padding=5, flex=1))
            status_item.add(toga.Label(text, style=Pack(font_size=12)))
            value_label = toga.Label('0', style=Pack(font_size=14, font_weight='bold'))
            status_item.add(value_label)
            self.status_labels[key] = value_label
            status_box.add(status_item)
        
        # Область проектов
        projects_box = toga.Box(style=Pack(direction=ROW, flex=1))
        
        # Активные проекты
        active_projects_box = toga.Box(style=Pack(direction=COLUMN, flex=1, padding=5))
        active_projects_box.add(toga.Label('АКТИВНЫЕ ПРОЕКТЫ', style=Pack(font_weight='bold')))
        self.active_projects_text = toga.MultilineTextInput(
            readonly=True,
            style=Pack(flex=1, background_color='#19232D')
        )
        active_projects_box.add(self.active_projects_text)
        
        # Очередь проектов
        queue_box = toga.Box(style=Pack(direction=COLUMN, flex=1, padding=5))
        queue_box.add(toga.Label('ОЧЕРЕДЬ ПРОЕКТОВ', style=Pack(font_weight='bold')))
        self.queue_text = toga.MultilineTextInput(
            readonly=True,
            style=Pack(flex=1, background_color='#19232D')
        )
        queue_box.add(self.queue_text)
        
        projects_box.add(active_projects_box)
        projects_box.add(queue_box)
        
        # Терминал
        terminal_box = toga.Box(style=Pack(direction=COLUMN, flex=2))
        terminal_box.add(toga.Label('ТЕРМИНАЛ', style=Pack(font_weight='bold')))
        self.terminal_text = toga.MultilineTextInput(
            readonly=True,
            style=Pack(flex=1, background_color='#0A0F19', color='#C8DCFF')
        )
        terminal_box.add(self.terminal_text)
        
        # Кнопки действий
        buttons_box = toga.Box(style=Pack(direction=ROW, flex_wrap='wrap', padding_top=10))
        
        actions = [
            ('Начать проект', self.start_project),
            ('Завершить проект', self.complete_project),
            ('Исправить баги', self.fix_bugs),
            ('Прокачать навык', self.learn_skill),
            ('Отдохнуть', self.rest),
            ('Очистить терминал', self.clear_terminal)
        ]
        
        for text, handler in actions:
            button = toga.Button(
                text,
                on_press=handler,
                style=Pack(padding=5, flex=1, background_color='#283848')
            )
            buttons_box.add(button)
        
        # Сборка интерфейса
        main_box.add(header)
        main_box.add(status_box)
        main_box.add(projects_box)
        main_box.add(terminal_box)
        main_box.add(buttons_box)
        
        # Начальное сообщение
        self.game.add_message("Запуск симулятора бэкенд-разработчика!", 'highlight')
        self.game.add_message("Нажмите кнопку для начала работы...", 'text')
        
        # Обновление интерфейса
        self.update_ui()
        
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def update_ui(self):
        # Обновление статуса
        self.status_labels['level'].text = f"{self.game.level}/{self.game.max_level}"
        self.status_labels['energy'].text = f"{self.game.energy}/{self.game.max_energy}"
        self.status_labels['money'].text = str(self.game.money)
        self.status_labels['reputation'].text = str(self.game.reputation)
        
        # Обновление проектов
        active_text = ""
        for i, project in enumerate(self.game.current_projects):
            active_text += f"{i+1}. {project['name']} (сложность: {project['difficulty']})\n"
        self.active_projects_text.value = active_text or "Нет активных проектов"
        
        queue_text = ""
        for i, project in enumerate(self.game.project_queue, 1):
            queue_text += f"{i}. {project['name']} (награда: {project['reward']})\n"
        self.queue_text.value = queue_text or "Очередь пуста"
        
        # Обновление терминала
        terminal_content = ""
        for message in self.game.message_log:
            terminal_content += f"{message['text']}\n"
        self.terminal_text.value = terminal_content

    def start_project(self, widget):
        result = self.game.start_project()
        if result:
            self.game.add_message(result[0], result[1])
        self.update_ui()

    def complete_project(self, widget):
        result = self.game.complete_project()
        if result:
            self.game.add_message(result[0], result[1])
        
        level_up = self.game.check_level_up()
        if level_up:
            self.game.add_message(level_up[0], level_up[1])
        
        self.update_ui()

    def fix_bugs(self, widget):
        result = self.game.fix_bugs()
        if result:
            self.game.add_message(result[0], result[1])
        self.update_ui()

    def learn_skill(self, widget):
        result = self.game.learn_skill()
        if result:
            self.game.add_message(result[0], result[1])
        self.update_ui()

    def rest(self, widget):
        result = self.game.rest()
        if result:
            self.game.add_message(result[0], result[1])
        self.update_ui()

    def clear_terminal(self, widget):
        self.game.message_log = []
        self.game.add_message("Терминал очищен", 'text')
        self.update_ui()


def main():
    return BackendSimulatorApp('Backend Developer Simulator', 'org.example.backendsim')


if __name__ == '__main__':
    app = main()
    app.main_loop()
